import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QRadioButton, QButtonGroup
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(250, 250, 700, 700)
        self.setWindowTitle('4')
        self.label_img = QLabel(self)
        self.label_img.move(50, 50)
        self.label_img.resize(600, 450)

        self.label = QLabel('Выберите тип карты:', self)
        self.label.move(50, 550)
        self.label.setFont(QFont("Times", 12))

        self.type = QButtonGroup()

        self.type_map = QRadioButton('map', self)
        self.type_map.setFont(QFont("Times", 12))
        self.type_map.move(50, 580)

        self.type_sat = QRadioButton('sat', self)
        self.type_sat.move(50, 600)
        self.type_sat.setFont(QFont("Times", 12))

        self.type_sat_skl = QRadioButton('sat_skl', self)
        self.type_sat_skl.move(50, 620)
        self.type_sat_skl.setFont(QFont("Times", 12))

        self.type.addButton(self.type_map)
        self.type.addButton(self.type_sat)
        self.type.addButton(self.type_sat_skl)

        self.btn = QPushButton('Применить', self)
        self.btn.move(50, 650)
        self.btn.resize(70, 25)
        self.btn.clicked.connect(self.types_cards)

        self.btn.setStyleSheet('QPushButton {background-color: #A3C1DA; color: green;}')

        self.api_server = "http://static-maps.yandex.ru/1.x/"
        self.qp = QPixmap()

        self.lon = "37.530887"
        self.lat = "55.703118"
        self.delta = "0.004"
        self.type_map_now = 'map'
        self.update_img()

    def types_cards(self):
        if self.type.checkedId() == -2:
            self.type_map_now = 'map'
        elif self.type.checkedId() == -3:
            self.type_map_now = 'sat'
        elif self.type.checkedId() == -4:
            self.type_map_now = 'sat,skl'
        self.update_img()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and float(self.delta) < 0.05:
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
            "l": self.type_map_now
        }
        response = requests.get(self.api_server, params=params)

        self.qp.loadFromData(response.content)
        self.label_img.setPixmap(self.qp)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())