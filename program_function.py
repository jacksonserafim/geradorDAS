import undetected_chromedriver as uc
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as SE
from validate_docbr import CNPJ
import re
import pandas as pd
from time import sleep


class ProgramFunction:
    def __init__(self, file_dir='', month_var='Janeiro', year_var='2023', column_entry=0, headless_var=False):
        from program_ui import window_alert
        self.window_alert = window_alert
        self.file = file_dir
        self.wait = None
        self.driver = None
        self.year = year_var
        self.month = month_var
        self.headless = headless_var
        self.columnEntry = column_entry
        self.doc_validation = CNPJ()
        self.report = open(f'RelatorioDAS-{self.month}-{self.year}.txt', 'a+', encoding="utf-8")
        self.monthsKey = {'Todos': 1, 'Janeiro': 2, 'Fevereiro': 3, 'Março': 4, 'Abril': 5, 'Maio': 6, 'Junho': 7,
                          'Julho': 8, 'Agosto': 9, 'Setembro': 10, 'Outubro': 11, 'Novembro': 12, 'Dezembro': 13}
        self.select_index = {'2018': 2, '2019': 3, '2020': 4, '2021': 5, '2022': 6, '2023': 7, '2024': 8}
        self.start_macro()

    def start_macro(self):
        try:
            spreadsheet = pd.read_excel(f'{self.file}', sheet_name=0)
        except:
            title = 'Erro ao ler a planilha'
            message = f'Houve problema ao tentar ler o arquivo'
            icon = 1
            self.window_alert(title, message, icon)
            self.driver.quit()
        else:
            self.driver = uc.Chrome(headless=self.headless, version_main=118)
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 10)
            self.iterate(spreadsheet)
            self.driver.quit()

    def iterate(self, spreadsheet):
        for index, row in spreadsheet.iterrows():
            cnpj = row.iloc[self.columnEntry]
            print(cnpj)
            print(type(cnpj))

            try:
                # Checagem se o CNPJ está com um formato válido
                if not self.doc_validation.validate(cnpj):
                    self.driver.quit()
                    self.report.write(f'{cnpj}  |  Erro')
                    raise ValueError(
                        f'CNPJ Inválido: {cnpj} \n Confira se o valor da coluna "CNPJ" está correta \nou se os dados inseridos são válidos')
            except ValueError as erro:
                self.window_alert('Erro de dado', erro, 2)
                raise StopIteration
            else:
                if cnpj in self.report:
                    print('PRESENTE')
                else:
                    # Conversão para somente números (Para não causar erro com o send_keys
                    cnpj = re.sub(r'[^0-9]', '', cnpj)
                    self.execute(cnpj, index + 2)

        self.report.close()

    def execute(self, cnpj, index):
        self.driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgmei.app/Identificacao')
        self.wait.until(lambda x: x.find_element(By.ID, 'cnpj')).send_keys(cnpj)
        self.wait.until(lambda x: x.find_element(By.ID, 'continuar')).click()

        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="navbarCollapse"]/ul[1]/li[2]/a')))

        except SE.TimeoutException:
            error_message = self.wait.until(
                lambda x: x.find_element(By.XPATH, '//*[@id="toast-container"]/div/div')).text
            if error_message == '13896 - Impedido por proteção Captcha. Comportamento de Robô.':
                self.driver.quit()
                self.start_macro()
                raise StopIteration

            elif error_message == '23008 - Contribuinte não optante pelo SIMEI.':
                self.report.write(
                    f'{index} | {self.doc_validation.mask(cnpj)}  |  Contribuinte não optante pelo SIMEI. 2 \n')

            elif error_message == '23007 - Base CNPJ indisponível. Tente novamente mais tarde.':
                message = 'Base CNPJ indisponível. Tente novamente mais tarde.'
                self.window_alert('Sistema indisponível', message, 1)


        else:
            self.wait.until(lambda x: x.find_element(By.XPATH, '//*[@id="navbarCollapse"]/ul[1]/li[2]/a')).click()
            self.wait.until(lambda x: x.find_element(By.XPATH,
                                                     '/html/body/div[1]/section[3]/div/div/div/div/div/form/div/div/button')).click()
            select_class = self.wait.until(lambda x: x.find_element(By.XPATH,
                                                                    f'/html/body/div[1]/section['f'3]/div/div/div/div/div/form/div/div/div'
                                                                    f'/ul/li['f'{self.select_index[self.year]}]')).get_attribute(
                'class')

            # Checagem se o CNPJ é optante ou não para o ano específico
            try:
                if select_class == 'disabled':
                    raise ValueError
            except TimeoutError:
                pass
            except ValueError:
                self.report.write(f'{index} | {self.doc_validation.mask(cnpj)}  |  Não Optante \n')

            else:
                self.wait.until(lambda x: x.find_element(By.XPATH, f"//*[contains(text(), '{self.year}')]")).click()
                self.wait.until(
                    lambda x: x.find_element(By.XPATH,
                                             '/html/body/div[1]/section[3]/div/div/div/div/div/form/button')).click()
                self.wait.until(
                    lambda x: x.find_element(By.XPATH,
                                             f'//*[@id="resumoDAS"]/table/tbody[{self.monthsKey[self.month]}]/tr/td[1]/input')).click()
                self.wait.until(lambda x: x.find_element(By.ID, 'btnEmitirDas')).click()

                self.wait.until(lambda x: x.find_element(By.XPATH,
                                                         '/html/body/div[1]/section[3]/div/div/div[1]/div/div/div[3]/div/div/a[1]')).click()
                self.wait.until(
                    lambda x: x.find_element(By.XPATH, '// *[ @ id = "toast-container"] / div / button')).click()
                self.report.write(f'{index} | {self.doc_validation.mask(cnpj)}  |  Emitido \n')
                sleep(2)


