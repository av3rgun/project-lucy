from PyQt5.QtWidgets import QGraphicsBlurEffect, QGraphicsDropShadowEffect
from datetime import datetime as dt, time as dt_time, timedelta as delta
from PyQt5 import QtCore, QtGui, QtWidgets
from deepl import translate
import http.client
import requests


class Ui_MainWindow(object):
    def __init__(self):
        self.color = "color: rgb(63, 229, 255, .8);"
        self.ip = self.get_ip()
        self.place = self.get_place()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setWindowIcon(QtGui.QIcon('../img/favicon.png'))
        MainWindow.setWindowTitle('Virtual Window')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.mainwidget = QtWidgets.QWidget(self.centralwidget)
        self.mainwidget.setGeometry(QtCore.QRect(0, 0, 1280, 720))
        self.mainwidget.setObjectName("mainwidget")

        self.weather_widget = QtWidgets.QWidget(self.mainwidget)
        self.weather_widget.setGeometry(QtCore.QRect(369, 52, 235, 305))
        self.weather_widget.setStyleSheet("#weather_widget{background-color: rgba(0, 0, 0, .3);}")
        self.weather_widget.setObjectName("weather_widget")

        # self.lucy_widget = QtWidgets.QWidget(self.mainwidget)
        # self.lucy_widget.setGeometry(QtCore.QRect(677, 362, 236, 307))
        # self.lucy_widget.setObjectName("lucy_widget")
        #
        # self.lucy_text = QtWidgets.QLabel(self.lucy_widget)
        # self.lucy_text.setGeometry(QtCore.QRect(0, 242, 235, 62))
        # self.lucy_text.setFont(self.nunito(10))
        # self.lucy_text.setStyleSheet(self.color)
        # self.lucy_text.setObjectName('lucy_text')
        # self.lucy_text.setGraphicsEffect(self.gen_shadow())

        self.time_label = QtWidgets.QLabel(self.weather_widget)
        self.time_label.setGeometry(QtCore.QRect(0, 3, 241, 31))
        self.time_label.setFont(self.nunito(20))
        self.time_label.setStyleSheet(self.color)
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.time_label.setObjectName("time_label")
        self.time_label.setGraphicsEffect(self.gen_shadow())
        self.time_label.raise_()

        self.date_label = QtWidgets.QLabel(self.weather_widget)
        self.date_label.setGeometry(QtCore.QRect(6, 25, 231, 31))
        self.date_label.setFont(self.nunito(14))
        self.date_label.setStyleSheet(self.color)
        self.date_label.setAlignment(QtCore.Qt.AlignCenter)
        self.date_label.setObjectName("date_label")
        self.date_label.setGraphicsEffect(self.gen_shadow())

        self.current_temp = QtWidgets.QLabel(self.weather_widget)
        self.current_temp.setGeometry(QtCore.QRect(10, 50, 55, 41))
        self.current_temp.setFont(self.nunito(25))
        self.current_temp.setStyleSheet(self.color)
        self.current_temp.setObjectName("current_temp")
        self.current_temp.setGraphicsEffect(self.gen_shadow())

        self.loc_icon = QtWidgets.QLabel(self.weather_widget)
        self.loc_icon.setGeometry(QtCore.QRect(10, 90, 16, 16))
        self.loc_icon.setFont(self.font_awesome(10))
        self.loc_icon.setStyleSheet(self.color)
        self.loc_icon.setObjectName("loc_icon")
        self.loc_icon.setGraphicsEffect(self.gen_shadow())

        self.place_label = QtWidgets.QLabel(self.weather_widget)
        self.place_label.setGeometry(QtCore.QRect(25, 89, 40, 16))
        self.place_label.setFont(self.nunito(11))
        self.place_label.setStyleSheet(self.color)
        self.place_label.setText(self.place)
        self.place_label.setObjectName("place_label")
        self.place_label.setGraphicsEffect(self.gen_shadow())

        self.status_icon = QtWidgets.QLabel(self.weather_widget)
        self.status_icon.setGeometry(QtCore.QRect(165, 60, 71, 16))
        self.status_icon.setFont(self.font_awesome(11))
        self.status_icon.setStyleSheet(self.color)
        self.status_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.status_icon.setObjectName("status_icon")
        self.status_icon.setGraphicsEffect(self.gen_shadow())

        self.status_text = QtWidgets.QLabel(self.weather_widget)
        self.status_text.setGeometry(QtCore.QRect(165, 75, 70, 16))
        self.status_text.setFont(self.nunito(10))
        self.status_text.setStyleSheet(self.color)
        self.status_text.setAlignment(QtCore.Qt.AlignCenter)
        self.status_text.setObjectName("status_text")
        self.status_text.setGraphicsEffect(self.gen_shadow())

        self.temp_max_min = QtWidgets.QLabel(self.weather_widget)
        self.temp_max_min.setGeometry(QtCore.QRect(165, 90, 70, 16))
        self.temp_max_min.setFont(self.nunito(10))
        self.temp_max_min.setStyleSheet(self.color)
        self.temp_max_min.setAlignment(QtCore.Qt.AlignCenter)
        self.temp_max_min.setObjectName("temp_max_min")
        self.temp_max_min.setGraphicsEffect(self.gen_shadow())

        self.forecast_time_1 = QtWidgets.QLabel(self.weather_widget)
        self.forecast_time_1.setGeometry(QtCore.QRect(10, 120, 21, 16))
        self.forecast_time_1.setFont(self.nunito(11))
        self.forecast_time_1.setStyleSheet(self.color)
        self.forecast_time_1.setObjectName("forecast_time_1")
        self.forecast_time_1.setGraphicsEffect(self.gen_shadow())

        self.forecast_status_1 = QtWidgets.QLabel(self.weather_widget)
        self.forecast_status_1.setGeometry(QtCore.QRect(10, 140, 21, 16))
        self.forecast_status_1.setFont(self.font_awesome(11))
        self.forecast_status_1.setStyleSheet(self.color)
        self.forecast_status_1.setObjectName("forecast_status_1")
        self.forecast_status_1.setGraphicsEffect(self.gen_shadow())

        self.forecast_temp_1 = QtWidgets.QLabel(self.weather_widget)
        self.forecast_temp_1.setGeometry(QtCore.QRect(10, 160, 22, 17))
        self.forecast_temp_1.setFont(self.nunito(11))
        self.forecast_temp_1.setStyleSheet(self.color)
        self.forecast_temp_1.setAlignment(QtCore.Qt.AlignCenter)
        self.forecast_temp_1.setObjectName("forecast_temp_1")
        self.forecast_temp_1.setGraphicsEffect(self.gen_shadow())

        self.forecast_temp_2 = QtWidgets.QLabel(self.weather_widget)
        self.forecast_temp_2.setGeometry(QtCore.QRect(50, 160, 22, 17))
        self.forecast_temp_2.setFont(self.nunito(11))
        self.forecast_temp_2.setStyleSheet(self.color)
        self.forecast_temp_2.setAlignment(QtCore.Qt.AlignCenter)
        self.forecast_temp_2.setObjectName("forecast_temp_2")
        self.forecast_temp_2.setGraphicsEffect(self.gen_shadow())

        self.forecast_time_2 = QtWidgets.QLabel(self.weather_widget)
        self.forecast_time_2.setGeometry(QtCore.QRect(50, 120, 21, 16))
        self.forecast_time_2.setFont(self.nunito(11))
        self.forecast_time_2.setAlignment(QtCore.Qt.AlignCenter)
        self.forecast_time_2.setStyleSheet(self.color)
        self.forecast_time_2.setObjectName("forecast_time_2")
        self.forecast_time_2.setGraphicsEffect(self.gen_shadow())

        self.forecast_status_2 = QtWidgets.QLabel(self.weather_widget)
        self.forecast_status_2.setGeometry(QtCore.QRect(50, 140, 21, 16))
        self.forecast_status_2.setFont(self.font_awesome(11))
        self.forecast_status_2.setStyleSheet(self.color)
        self.forecast_status_2.setAlignment(QtCore.Qt.AlignCenter)
        self.forecast_status_2.setObjectName("forecast_status_2")
        self.forecast_status_2.setGraphicsEffect(self.gen_shadow())

        self.forecast_time_3 = QtWidgets.QLabel(self.weather_widget)
        self.forecast_time_3.setGeometry(QtCore.QRect(90, 120, 21, 16))
        self.forecast_time_3.setFont(self.nunito(11))
        self.forecast_time_3.setStyleSheet(self.color)
        self.forecast_time_3.setAlignment(QtCore.Qt.AlignCenter)
        self.forecast_time_3.setObjectName("forecast_time_3")
        self.forecast_time_3.setGraphicsEffect(self.gen_shadow())

        self.forecast_temp_3 = QtWidgets.QLabel(self.weather_widget)
        self.forecast_temp_3.setGeometry(QtCore.QRect(90, 160, 22, 17))
        self.forecast_temp_3.setFont(self.nunito(11))
        self.forecast_temp_3.setStyleSheet(self.color)
        self.forecast_temp_3.setAlignment(QtCore.Qt.AlignCenter)
        self.forecast_temp_3.setObjectName("forecast_temp_3")
        self.forecast_temp_3.setGraphicsEffect(self.gen_shadow())

        self.forecast_status_3 = QtWidgets.QLabel(self.weather_widget)
        self.forecast_status_3.setGeometry(QtCore.QRect(90, 140, 21, 16))
        self.forecast_status_3.setFont(self.font_awesome(11))
        self.forecast_status_3.setStyleSheet(self.color)
        self.forecast_status_3.setAlignment(QtCore.Qt.AlignCenter)
        self.forecast_status_3.setObjectName("forecast_status_3")
        self.forecast_status_3.setGraphicsEffect(self.gen_shadow())

        self.forecast_temp_4 = QtWidgets.QLabel(self.weather_widget)
        self.forecast_temp_4.setGeometry(QtCore.QRect(130, 160, 22, 17))
        self.forecast_temp_4.setFont(self.nunito(11))
        self.forecast_temp_4.setStyleSheet(self.color)
        self.forecast_temp_4.setAlignment(QtCore.Qt.AlignCenter)
        self.forecast_temp_4.setObjectName("forecast_temp_4")
        self.forecast_temp_4.setGraphicsEffect(self.gen_shadow())

        self.forecast_time_4 = QtWidgets.QLabel(self.weather_widget)
        self.forecast_time_4.setGeometry(QtCore.QRect(130, 120, 21, 16))
        self.forecast_time_4.setFont(self.nunito(11))
        self.forecast_time_4.setStyleSheet("color: rgb(63, 229, 255);")
        self.forecast_time_4.setObjectName("forecast_time_4")
        self.forecast_time_4.setGraphicsEffect(self.gen_shadow())

        self.forecast_status_4 = QtWidgets.QLabel(self.weather_widget)
        self.forecast_status_4.setGeometry(QtCore.QRect(130, 140, 21, 16))
        self.forecast_status_4.setFont(self.font_awesome(11))
        self.forecast_status_4.setStyleSheet("color: rgb(63, 229, 255);")
        self.forecast_status_4.setAlignment(QtCore.Qt.AlignCenter)
        self.forecast_status_4.setObjectName("forecast_status_4")
        self.forecast_status_4.setGraphicsEffect(self.gen_shadow())

        self.forecast_status_5 = QtWidgets.QLabel(self.weather_widget)
        self.forecast_status_5.setGeometry(QtCore.QRect(170, 140, 21, 16))
        self.forecast_status_5.setFont(self.font_awesome(11))
        self.forecast_status_5.setStyleSheet(self.color)
        self.forecast_status_5.setAlignment(QtCore.Qt.AlignCenter)
        self.forecast_status_5.setObjectName("forecast_status_5")
        self.forecast_status_5.setGraphicsEffect(self.gen_shadow())

        self.forecast_temp_5 = QtWidgets.QLabel(self.weather_widget)
        self.forecast_temp_5.setGeometry(QtCore.QRect(170, 160, 22, 17))
        self.forecast_temp_5.setFont(self.nunito(11))
        self.forecast_temp_5.setStyleSheet(self.color)
        self.forecast_temp_5.setAlignment(QtCore.Qt.AlignCenter)
        self.forecast_temp_5.setObjectName("forecast_temp_5")
        self.forecast_temp_5.setGraphicsEffect(self.gen_shadow())

        self.forecast_time_5 = QtWidgets.QLabel(self.weather_widget)
        self.forecast_time_5.setGeometry(QtCore.QRect(170, 120, 21, 16))
        self.forecast_time_5.setFont(self.nunito(11))
        self.forecast_time_5.setStyleSheet(self.color)
        self.forecast_time_5.setObjectName("forecast_time_5")
        self.forecast_time_5.setAlignment(QtCore.Qt.AlignCenter)
        self.forecast_time_5.setGraphicsEffect(self.gen_shadow())

        self.forecast_status_6 = QtWidgets.QLabel(self.weather_widget)
        self.forecast_status_6.setGeometry(QtCore.QRect(210, 140, 21, 16))
        self.forecast_status_6.setFont(self.font_awesome(11))
        self.forecast_status_6.setStyleSheet(self.color)
        self.forecast_status_6.setAlignment(QtCore.Qt.AlignCenter)
        self.forecast_status_6.setObjectName("forecast_status_6")
        self.forecast_status_6.setGraphicsEffect(self.gen_shadow())

        self.forecast_time_6 = QtWidgets.QLabel(self.weather_widget)
        self.forecast_time_6.setGeometry(QtCore.QRect(210, 120, 21, 16))
        self.forecast_time_6.setFont(self.nunito(11))
        self.forecast_time_6.setStyleSheet(self.color)
        self.forecast_time_6.setAlignment(QtCore.Qt.AlignCenter)
        self.forecast_time_6.setObjectName("forecast_time_6")
        self.forecast_time_6.setGraphicsEffect(self.gen_shadow())

        self.forecast_temp_6 = QtWidgets.QLabel(self.weather_widget)
        self.forecast_temp_6.setGeometry(QtCore.QRect(210, 160, 22, 17))
        self.forecast_temp_6.setFont(self.nunito(11))
        self.forecast_temp_6.setStyleSheet(self.color)
        self.forecast_temp_6.setAlignment(QtCore.Qt.AlignCenter)
        self.forecast_temp_6.setObjectName("forecast_temp_6")
        self.forecast_temp_6.setGraphicsEffect(self.gen_shadow())

        self.alarm_time = QtWidgets.QLabel(self.weather_widget)
        self.alarm_time.setGeometry(QtCore.QRect(32, 285, 47, 16))
        self.alarm_time.setFont(self.nunito(13))
        self.alarm_time.setStyleSheet(self.color)
        self.alarm_time.setObjectName("alarm_time")
        self.alarm_time.setGraphicsEffect(self.gen_shadow())

        self.alarm_icon = QtWidgets.QLabel(self.weather_widget)
        self.alarm_icon.setGeometry(QtCore.QRect(10, 285, 21, 16))
        self.alarm_icon.setFont(self.font_awesome(11))
        self.alarm_icon.setStyleSheet(self.color)
        self.alarm_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.alarm_icon.setObjectName("alarm_icon")
        self.alarm_icon.setGraphicsEffect(self.gen_shadow())

        self.bulb_icon = QtWidgets.QLabel(self.weather_widget)
        self.bulb_icon.setGeometry(QtCore.QRect(210, 285, 21, 16))
        self.bulb_icon.setFont(self.font_awesome(11))
        self.bulb_icon.setStyleSheet(self.color)
        self.bulb_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.bulb_icon.setObjectName("bulb_icon")
        self.bulb_icon.setGraphicsEffect(self.gen_shadow())

        self.bulb_text = QtWidgets.QLabel(self.weather_widget)
        self.bulb_text.setGeometry(QtCore.QRect(186, 285, 25, 15))
        self.bulb_text.setFont(self.nunito(11))
        self.bulb_text.setStyleSheet(self.color)
        self.bulb_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.bulb_text.setObjectName("bulb_text")
        self.bulb_text.setGraphicsEffect(self.gen_shadow())

        self.cpu_icon = QtWidgets.QLabel(self.weather_widget)
        self.cpu_icon.setGeometry(QtCore.QRect(10, 265, 21, 16))
        self.cpu_icon.setFont(self.font_awesome(11))
        self.cpu_icon.setStyleSheet(self.color)
        self.cpu_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.cpu_icon.setObjectName("cpu_icon")
        self.cpu_icon.setGraphicsEffect(self.gen_shadow())

        self.ram_icon = QtWidgets.QLabel(self.weather_widget)
        self.ram_icon.setGeometry(QtCore.QRect(10, 245, 21, 16))
        self.ram_icon.setFont(self.font_awesome(11))
        self.ram_icon.setStyleSheet(self.color)
        self.ram_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.ram_icon.setObjectName("ram_icon")
        self.ram_icon.setGraphicsEffect(self.gen_shadow())

        self.btc_icon = QtWidgets.QLabel(self.weather_widget)
        self.btc_icon.setGeometry(QtCore.QRect(10, 225, 21, 16))
        self.btc_icon.setFont(self.font_awesome_brands(11))
        self.btc_icon.setStyleSheet(self.color)
        self.btc_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.btc_icon.setObjectName("btc_icon")
        self.btc_icon.setGraphicsEffect(self.gen_shadow())

        self.btc_text = QtWidgets.QLabel(self.weather_widget)
        self.btc_text.setGeometry(QtCore.QRect(35, 225, 61, 16))
        self.btc_text.setFont(self.nunito(11))
        self.btc_text.setStyleSheet(self.color)
        self.btc_text.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.btc_text.setObjectName("btc_text")
        self.btc_text.setGraphicsEffect(self.gen_shadow())

        self.ram_text = QtWidgets.QLabel(self.weather_widget)
        self.ram_text.setGeometry(QtCore.QRect(35, 245, 40, 16))
        self.ram_text.setFont(self.nunito(11))
        self.ram_text.setStyleSheet(self.color)
        self.ram_text.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.ram_text.setObjectName("ram_text")
        self.ram_text.setGraphicsEffect(self.gen_shadow())

        self.cpu_text = QtWidgets.QLabel(self.weather_widget)
        self.cpu_text.setGeometry(QtCore.QRect(35, 265, 40, 16))
        self.cpu_text.setFont(self.nunito(11))
        self.cpu_text.setStyleSheet(self.color)
        self.cpu_text.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.cpu_text.setObjectName("cpu_text")
        self.cpu_text.setGraphicsEffect(self.gen_shadow())

        self.movie_widget = QtWidgets.QWidget(self.mainwidget)
        self.movie_widget.setGeometry(QtCore.QRect(1280, 720, 1280, 720))
        self.movie_widget.setObjectName("movie_widget")

        self.videoframe = QtWidgets.QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.addWidget(self.videoframe)

        self.movie_widget.setLayout(self.vlayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

    @staticmethod
    def nunito(size):
        font = QtGui.QFont()
        font.setFamily("Nunito")
        font.setPointSize(size)
        font.setBold(True)
        font.setWeight(100)
        return font

    @staticmethod
    def font_awesome(size):
        font = QtGui.QFont()
        font.setFamily('Font Awesome 6 Free Solid')
        font.setPointSize(size)
        return font

    @staticmethod
    def font_awesome_brands(size):
        font = QtGui.QFont()
        font.setFamily('Font Awesome 6 Brands Regular')
        font.setPixelSize(size)
        return font

    @staticmethod
    def gen_shadow():
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QtGui.QColor(63, 229, 255))
        shadow.setBlurRadius(12)
        shadow.setOffset(0, 0)
        return shadow

    def showTime(self):
        current_time = QtCore.QTime.currentTime().toString('hh:mm')
        self.time_label.setText(current_time)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.loc_icon.setText(_translate("MainWindow", ""))
        self.alarm_time.setText(_translate("MainWindow", "13:13"))
        self.alarm_icon.setText(_translate("MainWindow", ""))
        self.bulb_icon.setText(_translate("MainWindow", ""))
        self.cpu_icon.setText(_translate("MainWindow", ""))
        self.ram_icon.setText(_translate("MainWindow", ""))
        self.btc_icon.setText(_translate("MainWindow", ""))
        self.btc_text.setText(_translate("MainWindow", "22590 $"))

    def generate_bg(self, bg=None):
        if bg is None:
            self.mainwidget.setStyleSheet("#mainwidget{background-color: "
                                          "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 "
                                          "rgba(170, 0, 127, 212), stop:1 rgba(85, 85, 127, 234));}")
        else:
            self.mainwidget.setStyleSheet("#mainwidget {background: url(img/" + bg + ".jpg) }")

    def set_date(self, date_string=None):
        if date_string is None:
            self.date_label.setText('13 Июня')
        else:
            self.date_label.setText(date_string)

    def set_place(self, place=None):
        if place is None:
            self.place_label.setText('Москва')
        else:
            self.place_label.setText(place)

    @staticmethod
    def get_ip():
        conn = http.client.HTTPConnection("ident.me")
        conn.request("GET", '/')
        ip = conn.getresponse().read().decode('utf-8')
        conn.close()
        return ip

    def get_place(self):
        try:
            resp = requests.get(url=f'http://ip-api.com/json/{self.ip}')
            r = resp.json()
            place = translate('EN', 'RU', text=r['city'])
            resp.close()
            return place
        except requests.ConnectionError as _ex:
            print(f'[Error]: {_ex}')

    def set_current_weather(self, values=None):
        if values is None:
            vals = {}
        else:
            vals = values

        self.current_temp.setText(vals['current_temp'])
        self.status_icon.setText(vals['status_icon'])
        self.status_text.setText(vals['status_text'])
        self.temp_max_min.setText(vals['temp_max_min'])

    def set_forecast(self, values):
        key = 1
        for el in values:
            for stamp, data in el.items():
                getattr(self, f'forecast_time_{key}').setText(dt.fromtimestamp(stamp).strftime("%H"))
                getattr(self, f'forecast_status_{key}').setText(self.get_weather_icon(stamp, data['status']))
                getattr(self, f'forecast_temp_{key}').setText(f'{round(data["temp"])}°')
                key += 1

    def get_weather_icon(self, stamp, status):
        pod = self.what_part_of_day(stamp)
        if pod == 'Ночь':
            word_bank = {
                '0': '', '1': '', '2': '', '3': '', '45': '', '48': '', '51': '', '53': '', '55': '',
                '56': '',
                '57': '', '61': '', '63': '', '65': '', '66': '', '67': '', '71': '', '73': '', '75': '',
                '77': '', '80': '', '81': '', '82': '', '85': '', '86': '', '95': '', '96': '', '99': ''
            }
        else:
            word_bank = {
                '0': '', '1': '', '2': '', '3': '', '45': '', '48': '', '51': '', '53': '', '55': '',
                '56': '',
                '57': '', '61': '', '63': '', '65': '', '66': '', '67': '', '71': '', '73': '', '75': '',
                '77': '', '80': '', '81': '', '82': '', '85': '', '86': '', '95': '', '96': '', '99': ''
            }
        for codes, icons in word_bank.items():
            if str(round(status)) == codes:
                icon = icons
                return icon

    def what_part_of_day(self, stamp):
        if self.time_in_range(dt_time(21, 0, 0), dt_time(4, 59, 59),
                              dt_time.fromisoformat(dt.fromtimestamp(stamp).strftime("%H:%M:%S"))) is True:
            pod = 'Ночь'
        elif self.time_in_range(dt_time(12, 0, 0), dt_time(17, 59, 59),
                                dt_time.fromisoformat(dt.fromtimestamp(stamp).strftime("%H:%M:%S"))) is True:
            pod = 'День'
        elif self.time_in_range(dt_time(5, 0, 0), dt_time(11, 59, 59),
                                dt_time.fromisoformat(dt.fromtimestamp(stamp).strftime("%H:%M:%S"))) is True:
            pod = 'Утро'
        elif self.time_in_range(dt_time(18, 0, 0), dt_time(20, 59, 59),
                                dt_time.fromisoformat(dt.fromtimestamp(stamp).strftime("%H:%M:%S"))) is True:
            pod = 'Вечер'
        else:
            pod = 'Hz'
        return pod

    @staticmethod
    def time_in_range(start, end, x):
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    def set_ram_usage(self, value):
        self.ram_text.setText(f'{value} %')

    def set_cpu_usage(self, value):
        self.cpu_text.setText(f'{value} %')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
