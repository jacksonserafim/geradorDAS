# :rocket: GeradorDAS

O **GeradorDAS** é uma ferramenta para automatizar a geração de Documentos de Arrecadação do Simples Nacional (DAS) a partir de uma planilha de CNPJs. Esta ferramenta utiliza Selenium para automatizar o processo de geração de DAS no site da Receita Federal.
O projeto ainda está em desenvolvimento e possui várias falhas e bugs, pois fiz com o intuito de ajudar um amigo e de quebra desenvolver minhas habilidades com Python, POO, automação e etc, qualquer sugestão ou dica é bem-vindo.
<p align="center">
  <img src="https://i.imgur.com/u1Zevjg.png?1" alt="Imagem da interface do Script">
</p>

## :gear: Como usar

### :white_check_mark: Pré-requisitos

Certifique-se de ter os seguintes requisitos instalados antes de usar o GeradorDAS:

- Python 3.10 ou superior:
- Bibliotecas Python necessárias (instaláveis via `pip`):
  - `undetected-chromedriver`
  - `selenium`
  - `validate-docbr`
  - `pandas`
  - `openpyxl`
  - `PyQt6` (para a interface gráfica)
  - `pyqt6-tools`  

### :inbox_tray: Instalação

Clone este repositório:

```
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto
```

Instale as dependências Python:

```
pip install -r requirements.txt
```

### :computer: Execução

Para executar o GeradorDAS, siga estas etapas:

1. Execute o arquivo `main.py`:

   ```
   python main.py
   ```

2. A interface gráfica será exibida, onde você poderá selecionar a planilha de CNPJs, o mês e o ano desejados. Também é possível escolher para que seja executado em segundo plano.

3. Clique no botão "Iniciar" para iniciar o processo de geração de DAS.

4. O GeradorDAS automatizará o processo de geração de DAS para os CNPJs listados na planilha e salvará um relatório no arquivo `RelatorioDAS-{mês}-{ano}.txt` onde o script for executado. (Os downloads são feitos na pasta padrão Downloads)

### :memo: Notas

- Para editar a interface é possível utilizar o Qt Designer que vem no pacote do pyqt6-tools, sendo necessário apenas abrir o arquivo `geradorDASgui.ui`, modificar e salvar, que na próxima vez que o script for executado, já contará com as modificações.

- O script é para baixar o Chrome Webdriver automaticamente porem certifique-se de que o Chrome WebDriver compatível com a versão 116 esteja instalado para evitar erros.

## :handshake: Contribuição

Se você deseja contribuir para o projeto, sinta-se à vontade para criar um fork deste repositório, fazer as alterações necessárias.
