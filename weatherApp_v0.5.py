# weather Application v0.5

import sys
import requests
from bs4 import BeautifulSoup

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

form_class = uic.loadUiType("ui/weatherAppUi.ui")[0]

class WeatherWin(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('오늘의 날씨')
        self.setWindowIcon(QIcon('icon/weather_icon.png'))
        self.statusBar().showMessage("Weather Application Ver0.5")

        self.weatherbtn.clicked.connect(self.request_weather)

    def request_weather(self):
        self.input_areaBox.text()# 사용자가 입력한 지역 이름을 가져오기
        weather_html = requests.get(f'https://search.naver.com/search.naver?&query={area}날씨')
        weather_soup = BeautifulSoup(weather_html.text, 'html.parser')

        area_text = weather_soup.find('h2', {'class': 'title'}).text

        self.area_label.setText(area_text) # area_label 레이블 자리에 area_text를 출력



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WeatherWin()
    win.show()
    sys,exit(app.exec_())