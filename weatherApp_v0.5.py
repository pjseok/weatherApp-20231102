# weather Application v0.5

import sys
import requests
from bs4 import BeautifulSoup

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import threading
import time

form_class = uic.loadUiType("ui/weatherAppUi.ui")[0]

class WeatherWin(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('오늘의 날씨')
        self.setWindowIcon(QIcon('icon/weather_icon.png'))
        self.statusBar().showMessage("Weather Application Ver0.5")
        self.setWindowFlags(Qt.WindowStaysOnTopHint) # 윈도우를 항상 맨 위에

        self.weatherbtn.clicked.connect(self.request_weather)
        self.weatherbtn.clicked.connect(self.reflashTimer)

    def request_weather(self):
        area = self.input_areaBox.text() # 사용자가 입력한 지역이름을 가져오기
        weather_html = requests.get(f'https://search.naver.com/search.naver?&query={area}날씨')
        weather_soup = BeautifulSoup(weather_html.text, 'html.parser')

        try:

            area_text = weather_soup.find('h2', {'class': 'title'}).text
            # 날씨를 조회하려는 지역주소 가져오기

            today_temperature = weather_soup.find('div', {'class': 'temperature_text'}).text  # 현재온도
            today_temperature = today_temperature[6:11]

            yesterday_weathertext = weather_soup.find('p', {'class': 'summary'}).text  # 어제온도와 현재온도의 비교
            yesterday_weathertext = yesterday_weathertext[:13].strip()

            sense_temperature = weather_soup.find('div', {'class': 'weather_info'}).find('dl', {'class': 'summary_list'}).find('dd', {'class': 'desc'}).text # 체감온도
            dust_info = weather_soup.select('ul.today_chart_list>li')
            dust1_info = dust_info[0].find('span', {'class': 'txt'}).text  # 미세먼지 정보
            dust2_info = dust_info[1].find('span', {'class': 'txt'}).text  # 초미세먼지 정보

            today_weathertext = weather_soup.find('span', {'class': 'weather before_slash'}).text  # 현재온도 텍스트

            self.setWeatherImage(today_weathertext)
            self.area_label.setText(area_text)  # area_label 레이블 자리에 area_text를 출력
            self.temper_label.setText(today_temperature)  # temper_label 레이블 자리에 today_temperature를 출력
            self.yesterday_label.setText(yesterday_weathertext)
            self.sense_temper.setText(sense_temperature) # 체감온도 출력
            self.dust1_label.setText(dust1_info) #미세먼지정보 출력
            self.dust2_label.setText(dust2_info) #초미세먼지정보 출력
        except Exception as e:
            print(e)
            self.area_label.setText('입력된 지역명 오류')

    def setWeatherImage(self, weatherText):
        # 날씨 종류 : 흐림, 맑음, 눈, 비, 구름많음, 기타
        if weatherText == '흐림':
            weatherImage = QPixmap("img/cloud.png")
            self.weather_label.setPixmap(QPixmap(weatherImage))
        elif weatherText == '맑음':
            weatherImage = QPixmap("img/sun.png")
            self.weather_label.setPixmap(QPixmap(weatherImage))
        elif weatherText == '눈':
            weatherImage = QPixmap("img/snow.png")
            self.weather_label.setPixmap(QPixmap(weatherImage))
        elif weatherText == '비':
            weatherImage = QPixmap("img/rain.png")
            self.weather_label.setPixmap(QPixmap(weatherImage))
        elif weatherText == '구름많음':
            weatherImage = QPixmap("img/cloud.png")
            self.weather_label.setPixmap(QPixmap(weatherImage))
        else:
            self.weather_label.setText(weatherText)


    def reflashTimer(self): # 자동 갱신
        self.request_weather()
        threading.Timer(60, self.reflashTimer).start()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WeatherWin()
    win.show()
    sys.exit(app.exec_())