import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication

from PyQt5.QtGui import QCursor


class BaseWidget(QWidget):
    """
    自定义窗口基类
    """

    def __init__(self, title):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle(title)
        self.setMinimumSize(400, 300)
        self.setCursor(Qt.ArrowCursor)  # 设置默认鼠标光标

        self.edge_size = 2  # 边缘大小
        self.dragging_edge = None  # 正在调整大小的边缘
        self.start_pos = None  # 鼠标按下时的位置
        self.window_pos = None  # 窗口位置

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.globalPos()
            self.window_pos = self.geometry().topLeft()

            # 判断是否处于边缘并设置鼠标光标
            x, y = event.x(), event.y()
            width, height = self.width(), self.height()
            if x < self.edge_size and y < self.edge_size:
                self.setCursor(Qt.SizeFDiagCursor)
                self.dragging_edge = Qt.TopLeftCorner
            elif x < self.edge_size and y > height - self.edge_size:
                self.setCursor(Qt.SizeBDiagCursor)
                self.dragging_edge = Qt.BottomLeftCorner
            elif x > width - self.edge_size and y < self.edge_size:
                self.setCursor(Qt.SizeBDiagCursor)
                self.dragging_edge = Qt.TopRightCorner
            elif x > width - self.edge_size and y > height - self.edge_size:
                self.setCursor(Qt.SizeFDiagCursor)
                self.dragging_edge = Qt.BottomRightCorner
            elif x < self.edge_size:
                self.setCursor(Qt.SizeHorCursor)
                self.dragging_edge = Qt.LeftEdge
            elif x > width - self.edge_size:
                self.setCursor(Qt.SizeHorCursor)
                self.dragging_edge = Qt.RightEdge
            elif y < self.edge_size:
                self.setCursor(Qt.SizeVerCursor)
                self.dragging_edge = Qt.TopEdge
            elif y > height - self.edge_size:
                self.setCursor(Qt.SizeVerCursor)
                self.dragging_edge = Qt.BottomEdge
            else:
                self.dragging_edge = None

    def mouseReleaseEvent(self, event):
        self.dragging_edge = None
        self.setCursor(Qt.ArrowCursor)

    def mouseMoveEvent(self, event):
        if self.dragging_edge is not None:
            delta = event.globalPos() - self.start_pos
            rect = self.geometry()

            if self.dragging_edge == Qt.LeftEdge:
                rect.setLeft(rect.left() + delta.x())
            elif self.dragging_edge == Qt.RightEdge:
                rect.setRight(rect.right() + delta.x())
            elif self.dragging_edge == Qt.TopEdge:
                rect.setTop(rect.top() + delta.y())
            elif self.dragging_edge == Qt.BottomEdge:
                rect.setBottom(rect.bottom() + delta.y())
            elif self.dragging_edge == Qt.TopLeftCorner:
                rect.setTopLeft(rect.topLeft() + delta)
            elif self.dragging_edge == Qt.TopRightCorner:
                rect.setTopRight(rect.topRight() + delta)
            elif self.dragging_edge == Qt.BottomLeftCorner:
                rect.setBottomLeft(rect.bottomLeft() + delta)
            elif self.dragging_edge == Qt.BottomRightCorner:
                rect.setBottomRight(rect.bottomRight() + delta)

            self.setGeometry(rect)
            self.start_pos = event.globalPos()
        else:
            # 没有处于边缘时，重置鼠标光标
            x, y = event.x(), event.y()
            width, height = self.width(), self.height()
            if x < self.edge_size and y < self.edge_size:
                self.setCursor(Qt.SizeFDiagCursor)
            elif x < self.edge_size and y > height - self.edge_size:
                self.setCursor(Qt.SizeBDiagCursor)
            elif x > width - self.edge_size and y < self.edge_size:
                self.setCursor(Qt.SizeBDiagCursor)
            elif x > width - self.edge_size and y > height - self.edge_size:
                self.setCursor(Qt.SizeFDiagCursor)
            elif x < self.edge_size:
                self.setCursor(Qt.SizeHorCursor)
            elif x > width - self.edge_size:
                self.setCursor(Qt.SizeHorCursor)
            elif y < self.edge_size:
                self.setCursor(Qt.SizeVerCursor)
            elif y > height - self.edge_size:
                self.setCursor(Qt.SizeVerCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

        super().mouseMoveEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = BaseWidget("窗口")
    widget.show()
    sys.exit(app.exec_())
