import threading

from PyQt5.QtGui import QTextCharFormat, QColor, QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import QTimer, Qt
import time


class OutputGenerator:
    def __init__(self, view):
        self.view: MainWindow = view

    def start(self, index):
        self.counter = 0
        while True:
            time.sleep(1)
            self.counter += 1
            if self.counter % 2:
                self.view.add_log(f"{index} Output 遥遥领先 {self.counter}")
            else:
                self.view.add_log(f"{index} Output {self.counter}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.btn = QPushButton("测试")
        self.btn.clicked.connect(self.start_output_generator)
        self.dynamic_monitor_text = QTextEdit()
        self.dynamic_monitor_text.setStyleSheet(
            'background-color: #f9f9f9; border: none; color: #333; font-size: 21px;')
        self.dynamic_monitor_text.setReadOnly(True)
        self.dynamic_monitor_text.setMinimumSize(1200, 666)
        layout.addWidget(self.btn)
        layout.addWidget(self.dynamic_monitor_text)
        self.setCentralWidget(central_widget)

    def add_log(self, output):
        cursor = QTextCursor(self.dynamic_monitor_text.document())
        format = QTextCharFormat()
        format.setForeground(Qt.black)  # 设置默认前景色为黑色
        cursor.movePosition(QTextCursor.End)

        start_index = output.find("遥遥领先")
        while start_index != -1:
            cursor.insertText(output[:start_index], format)  # 设置黑色样式
            cursor.insertText("遥遥领先", self.get_red_format())  # 设置红色样式
            output = output[start_index + len("遥遥领先"):]
            start_index = output.find("遥遥领先")

        cursor.insertText(output, format)  # 设置黑色样式
        cursor.insertBlock()

    def get_red_format(self):
        format = QTextCharFormat()
        format.setForeground(Qt.red)
        return format

    def start_output_generator(self):
        self.index += 1
        output_generator = OutputGenerator(self)
        thread = threading.Thread(target=output_generator.start, args=(f'线程{self.index}',), daemon=True)
        thread.start()


# 测试
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
