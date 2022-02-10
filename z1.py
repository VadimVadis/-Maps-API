import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QPixmap


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(250, 250, 700, 650)
        self.setWindowTitle('1')
        self.label = QLabel(self)
        self.label.move(50, 100)
        self.label.resize(600, 450)
        self.setStyleSheet("background-color: #14FFEC;")
        api_server = "http://static-maps.yandex.ru/1.x/"

        lon = "37.530887"
        lat = "55.703118"
        delta = "0.002"

        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([delta, delta]),
            "l": "map"
        }
        response = requests.get(api_server, params=params)

        qp = QPixmap()
        qp.loadFromData(response.content)
        self.label.setPixmap(qp)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
