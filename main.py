from program_ui import MainWindow, QApplication


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
