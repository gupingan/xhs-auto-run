from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QTextCursor, QTextCharFormat
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton


class SeleniumWrapper:
    def __init__(self):
        options_dict = {
            "disable-blink-features": "AutomationControlled",
            "excludeSwitches": ["enable-automation"],
            "ignore-certificate-errors": True,
            "window-size": "1250,900",
            "no-sandbox": True
        }
        options = Options()
        for key, value in options_dict.items():
            options.add_argument(f"--{key}={value}")
        service = Service(executable_path='./chromedriver.exe')
        self.driver = webdriver.Chrome(service=service)

    def open_url(self, url):
        self.driver.get(url)

    def find_element(self, selector):
        return self.driver.find_element(*selector)

    def find_elements(self, selector):
        return self.driver.find_elements(*selector)

    def close(self):
        self.driver.quit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.btn = QPushButton("测试")
        layout.addWidget(self.btn)
        self.setCentralWidget(central_widget)


if __name__ == '__main__':
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()
