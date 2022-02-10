import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QRadioButton, QButtonGroup, QCheckBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(250, 250, 1000, 700)
        self.setWindowTitle('9')
        self.label_img = QLabel(self)
        self.label_img.move(50, 20)
        self.label_img.resize(450, 450)
        # Ввод адреса и поиск
        self.label = QLabel('Введите адрес:', self)
        self.label.move(600, 20)
        self.label.setFont(QFont("Times", 12))

        self.place_input = QLineEdit(self)
        self.place_input.move(600, 50)
        self.place_input.resize(300, 25)
        self.place_input.setText('Воронеж, Университетская площадь, 1')

        self.btn_change = QPushButton('Искать', self)
        self.btn_change.move(910, 50)
        self.btn_change.resize(70, 25)
        self.btn_change.clicked.connect(self.update_address_img)
        self.btn_change.setStyleSheet('QPushButton {background-color: #A3C1DA; color: green;}')
        # Выбор типа карты
        self.label = QLabel('Выберите тип карты:', self)
        self.label.move(50, 520)
        self.label.setFont(QFont("Times", 12))

        self.type = QButtonGroup()

        self.type_map = QRadioButton('map', self)
        self.type_map.setFont(QFont("Times", 12))
        self.type_map.move(50, 550)

        self.type_sat = QRadioButton('sat', self)
        self.type_sat.move(50, 570)
        self.type_sat.setFont(QFont("Times", 12))

        self.type_sat_skl = QRadioButton('sat_skl', self)
        self.type_sat_skl.move(50, 590)
        self.type_sat_skl.setFont(QFont("Times", 12))

        self.type.addButton(self.type_map)
        self.type.addButton(self.type_sat)
        self.type.addButton(self.type_sat_skl)
        #Сброс метки
        self.btn_reset = QPushButton('Сброс\nметки', self)
        self.btn_reset.move(450, 470)
        self.btn_reset.resize(50, 50)
        self.btn_reset.clicked.connect(self.reset_metka)

        self.btn_map = QPushButton('Применить', self)
        self.btn_map.move(50, 620)
        self.btn_map.resize(70, 25)
        self.btn_map.clicked.connect(self.types_cards)
        self.btn_map.setStyleSheet('QPushButton {background-color: #A3C1DA; color: green;}')
        # Точный адрес найденного объекта
        self.exact_address = QLineEdit(self)
        self.exact_address.move(600, 150)
        self.exact_address.resize(350, 25)
        self.exact_address.setDisabled(True)

        self.label = QLabel('Полный адрес:', self)
        self.label.move(600, 120)
        self.label.setFont(QFont("Times", 12))

        self.edit_index = QCheckBox('Почтовый индекс', self)
        self.edit_index.move(600, 185)

        self.geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        self.api_server = "http://static-maps.yandex.ru/1.x/"

        self.qp = QPixmap()

        self.lon = "37.530887"
        self.lat = "55.703118"
        self.lon_metka = self.lon
        self.lat_metka = self.lat
        self.delta = "0.005"
        self.type_map_now = 'map'
        self.metka = True
        self.update_address_img()

    def reset_metka(self):
        self.metka = False
        self.exact_address.setText('')
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
        if event.key() == Qt.Key_PageUp and float(self.delta) < 0.5:
            self.delta = str(float(self.delta) + 0.005)
        elif event.key() == Qt.Key_PageDown and float(self.delta) > 0.0051:
            self.delta = str(float(self.delta) - 0.005)

        if event.key() == Qt.Key_Left:
            self.lon = str(float(self.lon) - float(self.delta))
        elif event.key() == Qt.Key_Up:
            self.lat = str(float(self.lat) + float(self.delta))
        elif event.key() == Qt.Key_Right:
            self.lon = str(float(self.lon) + float(self.delta))
        elif event.key() == Qt.Key_Down:
            self.lat = str(float(self.lat) - float(self.delta))
        self.update_img()

    def update_address_img(self):
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": self.place_input.text(),
            "format": "json"}

        response = requests.get(self.geocoder_api_server, params=geocoder_params)

        if not response:
            pass

        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]

        exact_address = toponym['metaDataProperty']['GeocoderMetaData']['AddressDetails'][
            'Country']['AddressLine']
        if self.edit_index.checkState():
            exact_address += ', ' + str(toponym['metaDataProperty']['GeocoderMetaData']['Address'][
                'postal_code'])
        self.exact_address.setText(exact_address)
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        self.lat_metka, self.lat = toponym_lattitude, toponym_lattitude
        self.lon_metka, self.lon = toponym_longitude, toponym_longitude
        self.delta = "0.005"
        self.metka = True
        self.update_img()

    def update_img(self):
        if self.metka:
            params = {
                "ll": ",".join([self.lon, self.lat]),
                "spn": ",".join([self.delta, self.delta]),
                "pt": ",".join([self.lon_metka, self.lat_metka, 'pmgnm']),
                "l": self.type_map_now,
                "size": "450,450"
            }
        else:
            params = {
                "ll": ",".join([self.lon, self.lat]),
                "spn": ",".join([self.delta, self.delta]),
                "l": self.type_map_now,
                "size": "450,450"
            }
        response = requests.get(self.api_server, params=params)

        self.qp.loadFromData(response.content)
        self.label_img.setPixmap(self.qp)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
