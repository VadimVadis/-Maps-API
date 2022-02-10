import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(250, 250, 700, 650)
        self.setWindowTitle('3')
        self.label = QLabel(self)
        self.label.move(50, 100)
        self.label.resize(600, 450)
        self.setStyleSheet("background-color: #14FFEC;")
        self.api_server = "http://static-maps.yandex.ru/1.x/"
        self.qp = QPixmap()

        self.lon = "37.530887"
        self.lat = "55.703118"
        self.delta = "0.004"
        self.update_img()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and float(self.delta) < 0.040:
            self.delta = str(float(self.delta) + 0.004)
        elif event.key() == Qt.Key_PageDown and float(self.delta) > 0.0041:
            self.delta = str(float(self.delta) - 0.004)

        if event.key() == Qt.Key_Left:
            self.lon = str(float(self.lon) - float(self.delta))
        if event.key() == Qt.Key_Up:
            self.lat = str(float(self.lat) + float(self.delta))
        if event.key() == Qt.Key_Right:
            self.lon = str(float(self.lon) + float(self.delta))
        if event.key() == Qt.Key_Down:
            self.lat = str(float(self.lat) - float(self.delta))
        self.update_img()

    def update_img(self):
        params = {
            "ll": ",".join([self.lon, self.lat]),
            "spn": ",".join([self.delta, self.delta]),
            "l": "map"
        }
        response = requests.get(self.api_server, params=params)

        self.qp.loadFromData(response.content)
        self.label.setPixmap(self.qp)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())