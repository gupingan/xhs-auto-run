import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton, QMenu, QAction, QMessageBox
from PyQt5.QtCore import Qt, QThread


class WorkerThread(QThread):
    def __init__(self, thread_id, parent=None):
        super().__init__(parent)
        self.thread_id = thread_id

    def run(self):
        print("Thread ID:", self.thread_id)
        self.exec_()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.button = QPushButton("创建线程")

        self.init_ui()

    def init_ui(self):
        self.setLayout(self.layout)

        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.create_thread)
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)

    def create_thread(self):
        thread_id = len(self.children())  # 使用子控件数量作为线程 ID
        thread = WorkerThread(thread_id)
        item_text = f"线程名: Thread{thread_id}, 线程ID: {thread.thread_id}"
        self.list_widget.addItem(item_text)
        thread.start()

    def show_context_menu(self, position):
        item = self.list_widget.itemAt(position)
        if item:
            menu = QMenu(self.list_widget)

            close_action = QAction("关闭线程", self.list_widget)
            close_action.triggered.connect(lambda: self.close_thread(item))
            menu.addAction(close_action)

            menu.exec_(self.list_widget.mapToGlobal(position))

    def close_thread(self, item):
        thread_id = int(item.text().split(":")[-1].strip())  # 获取线程 ID
        thread = self.findChild(QThread, f"WorkerThread{thread_id}")

        if thread:
            confirm = QMessageBox.question(self, "关闭线程", "确定要关闭该线程吗？",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                thread.quit()
                thread.wait()
                self.list_widget.takeItem(self.list_widget.row(item))
        else:
            QMessageBox.warning(self, "错误", "未找到该线程")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
