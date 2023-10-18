import threading

from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QTextCursor, QTextCharFormat
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton


class OutputGenerator(QObject):
    output_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def start(self, index):
        self.counter = 0
        while True:
            self.counter += 1
            if self.counter % 2:
                self.output_signal.emit(f"{index} Output 遥遥领先 {self.counter}")
            else:
                self.output_signal.emit(f"{index} Output 一马难追！ {self.counter}。。。。。。。。")
            # 模拟计算或IO密集型任务
            self.msleep(500)

    def msleep(self, interval):
        from time import sleep
        sleep(interval / 1000)


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
        self.dynamic_monitor_text.setLineWrapMode(QTextEdit.NoWrap)
        self.dynamic_monitor_text.setStyleSheet(
            'background-color: #f9f9f9; border: none; color: #333; font-size: 21px;')
        self.dynamic_monitor_text.setReadOnly(True)
        self.dynamic_monitor_text.setMinimumSize(400, 300)
        layout.addWidget(self.btn)
        layout.addWidget(self.dynamic_monitor_text)
        self.setCentralWidget(central_widget)
        self.dynamic_monitor_text.verticalScrollBar().rangeChanged.connect(self.change_scroll)

    def change_scroll(self, min, max):
        current = self.dynamic_monitor_text.verticalScrollBar().value()
        if self.before <= current <= self.after:
            self.dynamic_monitor_text.verticalScrollBar().setValue(max)
        else:
            self.dynamic_monitor_text.verticalScrollBar().setValue(current)

    def add_log(self, output):
        self.before = self.dynamic_monitor_text.verticalScrollBar().maximum()
        cursor = QTextCursor(self.dynamic_monitor_text.document())
        format = self.get_format(Qt.black)
        cursor.movePosition(QTextCursor.End)
        start_index = output.find("遥遥领先")
        while start_index != -1:
            cursor.insertText(output[:start_index], format)  # 设置黑色样式
            cursor.insertText("遥遥领先", self.get_format(Qt.red))  # 设置红色样式
            output = output[start_index + len("遥遥领先"):]
            start_index = output.find("遥遥领先")
        success_index = output.find("一马难追！")
        while success_index != -1:
            cursor.insertText(output[:success_index], format)  # 设置黑色样式
            cursor.insertText("一马难追！", self.get_format(Qt.green))  # 设置绿色样式
            output = output[success_index + 5:]
            success_index = output.find("一马难追！")
        cursor.insertText(output, format)  # 设置黑色样式
        cursor.insertBlock()
        self.after = self.dynamic_monitor_text.verticalScrollBar().maximum()

    def get_format(self, color):
        format = QTextCharFormat()
        format.setForeground(color)
        return format

    def start_output_generator(self):
        self.index += 1
        output_generator = OutputGenerator()
        output_generator.output_signal.connect(self.add_log)
        thread = threading.Thread(target=output_generator.start, args=(f'线程{self.index}',), daemon=True)
        thread.start()


if __name__ == '__main__':
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()
