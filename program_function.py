import undetected_chromedriver as uc
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.wait import WebDriverWait
import re
import pandas as pd
from time import sleep


class ProgramFunction:
    def __init__(self, file_dir='', month_var='Janeiro', year_var='2023', column_entry=0, headless_var=False):
        self.file = file_dir
        self.wait = None
        self.driver = None
        self.year = year_var
        self.month = month_var
        self.headless = headless_var
        self.columnEntry = column_entry
        self.monthsKey = {'Todos': 1, 'Janeiro': 2, 'Fevereiro': 3, 'Março': 4, 'Abril': 5, 'Maio': 6, 'Junho': 7,
                          'Julho': 8, 'Agosto': 9, 'Setembro': 10, 'Outubro': 11, 'Novembro': 12, 'Dezembro': 13}
        self.start_macro()

    def start_macro(self):
        self.driver = uc.Chrome(headless=self.headless)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)
        self.read(file=self.file)

    def read(self, file):
        spredsheet: pd.DataFrame
        try:
            spreadsheet = pd.read_excel(f'{file}', engine='openpyxl', sheet_name=0)
            self.iterate(spreadsheet)
        except Exception as e:
            from program_ui import MainWindow
            msg = MainWindow()
            title = 'Erro ao ler a planilha'
            message = f'Houve problema ao tentar ler o arquivo {e}'
            icon = 1
            msg.window_alert(title, message, icon)

    def iterate(self, spreadsheet):
        for index, row in spreadsheet.iterrows():
            cnpj = row.iloc[self.columnEntry]
            cnpj = re.sub(r'[^0-9]', '', cnpj)

            self.execute(cnpj=cnpj)

        self.driver.quit()

    def execute(self, cnpj):
        self.driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgmei.app/Identificacao')
        self.wait.until(lambda x: x.find_element(By.ID, 'cnpj')).send_keys(cnpj)
        self.wait.until(lambda x: x.find_element(By.ID, 'continuar')).click()

        self.wait.until(lambda x: x.find_element(By.XPATH, '//*[@id="navbarCollapse"]/ul[1]/li[2]/a')).click()
        self.wait.until(lambda x: x.find_element(By.XPATH,
                                                 '/html/body/div[1]/section[3]/div/div/div/div/div/form/div/div/button')).click()
        self.wait.until(lambda x: x.find_element(By.XPATH, f"//*[contains(text(), '{self.year}')]")).click()
        self.wait.until(
            lambda x: x.find_element(By.XPATH, '/html/body/div[1]/section[3]/div/div/div/div/div/form/button')).click()
        self.wait.until(
            lambda x: x.find_element(By.XPATH,
                                     f'//*[@id="resumoDAS"]/table/tbody[{self.monthsKey[self.month]}]/tr/td[1]/input')).click()
        self.wait.until(lambda x: x.find_element(By.ID, 'btnEmitirDas')).click()

        self.wait.until(lambda x: x.find_element(By.XPATH,
                                                 '/html/body/div[1]/section[3]/div/div/div[1]/div/div/div[3]/div/div/a[1]')).click()
        self.wait.until(lambda x: x.find_element(By.XPATH, '// *[ @ id = "toast-container"] / div / button')).click()
        sleep(2)

    def close_driver(self):
        self.driver.quit()
