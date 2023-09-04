from pathlib import Path
from PyQt6 import QtGui
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from program_function import ProgramFunction


class MainWindow(QMainWindow):

    def __init__(self):
        # LoadUI
        super(MainWindow, self).__init__()
        self.path = None
        self.setWindowIcon(QtGui.QIcon('src/logo.png'))
        loadUi('src/geradorDASgui.ui', self)
        self.show()

        months = ['Janeiro', 'Fevereiro', 'Março',
                  'Abril', 'Maio', 'Junho',
                  'Julho', 'Agosto', 'Setembro',
                  'Outubro', 'Novembro', 'Dezembro']
        self.monthOptions.addItems(months)

        years = ['2023', '2024', '2025']
        self.yearOptions.addItems(years)

        self.fileSelectorBtn.clicked.connect(self.select_file)

        self.startBtn.clicked.connect(self.start_script)

    def select_file(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            caption="Selecione a planilha",
            filter="Planilhas (*.xls *.xlsx)",
            directory='C:'
        )
        if filename:
            self.path = Path(filename)
            self.filePath.setText(f'Planilha: {self.path}')
            self.fileSelectorBtn.setText('Trocar documento')

    def start_script(self):
        try:
            month = self.monthOptions.currentText()
            year = self.yearOptions.currentText()
            column = self.columnEntry.value()
            headless = self.headlessCheck.isChecked()
            try:
                ProgramFunction(file_dir=self.path, month_var=month, year_var=year, column_entry=column,
                                headless_var=headless)
            except Exception as e:
                title = 'Erro'
                message = f'Erro ao iniciar ou executar o script {e}'
                icon = 1
                self.window_alert(title, message, icon)

            title = 'Concluído'
            message = 'Todos os DAS emitidos e downloads concluídos'
            icon = 0
            self.window_alert(title, message, icon)
        except Exception as e:
            title = 'Erro'
            message = f'Erro ao iniciar ou executar o script {e}'
            icon = 1
            self.window_alert(title, message, icon)

    def window_alert(self, title, message, icon):
        msg = QMessageBox(parent=self)
        msg.setWindowTitle(f'{title}')
        msg.setText(f'{message}')
        match icon:
            case 0:
                msg.setIcon(QMessageBox.Icon.Information)
            case 1:
                msg.setIcon(QMessageBox.Icon.Warning)
            case 2:
                msg.setIcon(QMessageBox.Icon.Critical)
            case 3:
                msg.setIcon(QMessageBox.Icon.Question)
        msg.show()
