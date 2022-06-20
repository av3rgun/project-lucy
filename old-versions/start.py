from datetime import datetime as dt, time as dt_time, timedelta as delta
from vosk import Model, KaldiRecognizer, SetLogLevel
from modules.design import Ui_MainWindow as Design
from yeelight import discover_bulbs, Bulb
from PyQt5.QtWidgets import QMainWindow
from modules.weather import Weather
from PyQt5 import QtWidgets, QtGui
from modules.player import Player
import speech_recognition as sr
from threading import Thread
from fuzzywuzzy import fuzz
from deepl import translate
from random import choice
from colorama import Fore
from time import sleep
import schedule
import winsound
import pyttsx3
import wave
import json
import vlc
import sys
import os


class Assistant:
    def __init__(self, player, window, weather):
        self.name = 'люси'
        self.alias = (self.name, 'ляся', 'люсяш', 'люсия', 'луси', 'люська', 'люся')
        self.logging = SetLogLevel(-1)
        self.engine = pyttsx3.init()
        self.player = player
        self.window = window
        self.weather = weather
        self.stop_process = False
        self.thread = Thread(target=self.checking_thread, args=(lambda: self.stop_process, ), daemon=True)
        self.thread.start()
        self.text = ''
        self.answer = ''
        self.opts = {
            "tbr": ('включи', 'выключи', 'открой', 'закрой', 'зайди', 'найди', 'сделай', 'запусти'),
            "cmds": {('привет', 'здравствуй', 'приветствую', 'хай', 'ну привет'): self.hello,
                     ('радио', 'radio'): self.radio,
                     ('громкость', 'звук'): self.set_volume,
                     ('канал',): self.channel,
                     ('стоп', 'stop'): self.quit,
                     ('интерфейс', 'interface'): self.interface,
                     ('систему',): self.system_start,
                     ('яркость', ): self.brightness,
                     ('свет', ): self.luminosity,
                     }
        }
        self.owner_name = 'Александр'
        self.pod = self.part_of_day()
        self.action = ''
        self.option = ''
        self.date = self.get_date()
        self.bulb = self.get_bulb()
        self.check_system()

    def offline_recognition(self):
        try:
            if not os.path.exists("models/vosk-model-small-ru-0.22"):
                print(Fore.RED + "Please download the model from:\n" +
                      "https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
                exit(1)

            wave_audio = wave.open('cache/last-recognized.wav', 'rb')
            model = Model("models/vosk-model-small-ru-0.22")
            offline_recognizer = KaldiRecognizer(model, wave_audio.getframerate())

            data = wave_audio.readframes(wave_audio.getnframes())
            if len(data) > 0:
                if offline_recognizer.AcceptWaveform(data):
                    recognizer_data = offline_recognizer.Result()
                    recognizer_data = json.loads(recognizer_data)
                    self.text = recognizer_data['text']
        except Exception as _ex:
            print(Fore.RED + f'[Error]: {_ex}')
        return self.text

    @staticmethod
    def get_bulb():
        bulb_ip = discover_bulbs()[0]['ip']
        bulb = Bulb(bulb_ip)
        return bulb

    def wake_up(self):
        with sr.Microphone() as micro:
            recognize = sr.Recognizer()
            recognize.adjust_for_ambient_noise(micro, 2)
            try:
                print("Listening..")
                audio = recognize.listen(micro, 2, 2)
                with open('cache/last-recognized.wav', 'wb') as file:
                    file.write(audio.get_wav_data())

            except sr.WaitTimeoutError:
                return

            try:
                self.text = recognize.recognize_google(audio, language='ru-RU').lower()
                if self.text in self.alias:
                    self.response()
                    self.recognize()

            except sr.UnknownValueError:
                return

            except sr.RequestError:
                print('Using offline recognition..')
                self.text = self.offline_recognition()

            return self.text

    def recognize(self):
        with sr.Microphone() as micro:
            recognize = sr.Recognizer()
            recognize.adjust_for_ambient_noise(micro, 0.5)
            try:
                print("Listening..")
                audio = recognize.listen(micro, 5, 5)
                with open('cache/last-recognized.wav', 'wb') as file:
                    file.write(audio.get_wav_data())

            except sr.WaitTimeoutError:
                self.speak("Проверьте свой микрофон. Возможно он не распознаётся!")
                return

            try:
                self.text = recognize.recognize_google(audio, language='ru-RU').lower()
                print(Fore.GREEN + f'Вы сказали: {self.text}' + Fore.RESET)
                for action in self.opts['tbr']:
                    if self.text.startswith(self.opts['tbr']):
                        com = self.text.replace(action, '').strip()
                        if self.text != com:
                            new_action = self.text.replace(com, '').strip()
                            self.action = new_action
                            self.text = com
                for tasks in self.opts['cmds']:
                    for task in tasks:
                        option = self.text.replace(task, '').strip()
                        if self.text != option:
                            self.option = option
                            new_cmd = self.text.replace(option, '').strip()
                            self.text = new_cmd
                            if fuzz.ratio(task, self.text) >= 99:
                                command_option = [self.option]
                                command_option.insert(0, self.action)
                                self.opts['cmds'][tasks](command_option)
                                self.action = ''
                                self.option = ''

            except sr.UnknownValueError:
                self.speak('Простите, не могли бы вы повторить?')

            except sr.RequestError:
                print('Using offline recognition..')
                self.text = self.offline_recognition()

            return self.text

    def speak(self, text):
        print(Fore.CYAN + f'[EVA]: {text}' + Fore.RESET)
        self.engine.say(text)
        self.engine.runAndWait()
        self.engine.stop()

    @staticmethod
    def response():
        file = 'sounds/response1.wav'
        winsound.PlaySound(file, winsound.SND_FILENAME | winsound.SND_ASYNC)

    @staticmethod
    def get_date():
        day = dt.now().day
        month = dt.now().month
        month_f = translate('EN', 'RU', text=dt.now().strftime("%B"))
        if month == 3 or month == 8:
            month_s = f'{month_f}a'
        else:
            month_s = month_f.replace(month_f[-1], 'я')
        return f'{day} {month_s}'

    def hello(self, *args: list):
        answer = ['Привет', f'Здравствуйте, {self.owner_name}', f'Добрый {self.pod.lower()}',
                  f'И Вам не хворать, {self.owner_name}']
        self.speak(choice(answer))

    def radio(self, *args: list):
        if args[0][1]:
            self.speak(f'Включаю радио {args[0][1]}')
            self.player.select_station(args[0][1])
        if args[0][0] == "включи":
            self.player.play()
        elif args[0][0] == 'выключи':
            self.player.stop()

    def channel(self, *args: list):
        if args[0][1]:
            self.speak(f'Включаю телеканал {args[0][1]}')
            self.player.select_channel(args[0][1])
        if args[0][0] == 'включи':
            self.player.player.set_hwnd(int(self.window.videoframe.winId()))
            self.player.play()
            self.window.movie_widget.move(0, 0)
        elif args[0][0] == 'выключи':
            self.player.stop()
            self.window.movie_widget.move(1280, 720)

    def set_volume(self, *args: list):
        current_volume = self.player.get_volume()
        numbers = {
            'один': 1, 'два': 2, 'три': 3, 'четыре': 4, 'пять': 5,
            'шесть': 6, 'семь': 7, 'восемь': 8, 'девять': 9, 'десять': 10
        }
        if not args[0][1].isdigit():
            for word, number in numbers.items():
                if args[0][1] == word:
                    vol = number
                    if current_volume == vol * 10:
                        self.speak('Ничего не изменилось!')
                    else:
                        self.player.set_volume(vol * 10)
        else:
            if current_volume == int(args[0][1]) * 100:
                self.speak('Ничего не изменилось!')
            else:
                self.player.set_volume(int(args[0][1]) * 10)

    def quit(self, *args):
        self.speak(f'До свидания {self.owner_name}!')
        sleep(1)
        sys.exit(1)

    def system_start(self, *args):
        self.speak('Инициализация системы')
        self.speak('Запуск необходимых параметров')
        self.speak('Проверка работоспособности')
        self.speak('Все процессы успешно запущены. Приятного пользования!')

    def routine(self):
        """Запуск автоматического обновления данных в фоне!"""
        pass

    def interface(self, *args):
        self.set_default_data()
        self.window.show()

    def set_default_data(self):
        vals = self.weather.create_current_dict()
        self.window.generate_bg(self.weather.set_background())
        self.window.place_label.setText(self.window.place)
        self.window.date_label.setText(self.date)
        self.window.current_temp.setText(vals['current_temp'])
        self.window.status_icon.setText(vals['status_icon'])
        self.window.status_text.setText(vals['status_text'])
        self.window.temp_max_min.setText(vals['temp_max_min'])
        forecast = self.weather.near_forecast()
        key = 1
        for el in forecast:
            for stamp, data in el.items():
                getattr(self.window, f'forecast_time_{key}').setText(dt.fromtimestamp(stamp).strftime("%H"))
                getattr(self.window, f'forecast_status_{key}').setText(self.weather.get_weather_icon(stamp,
                                                                                                     data['status']))
                getattr(self.window, f'forecast_temp_{key}').setText(f'{round(data["temp"])}°')
                key += 1

    def brightness(self, *args: list):
        bright = args[0][1]
        perc = int(bright.replace('%', ''))
        self.bulb.set_brightness(perc)

    def luminosity(self, *args: list):
        if args[0][0] == 'включи':
            if self.bulb.turn_on() == 'ok':
                self.window.bulb_icon.setText('')
                self.window.bulb_text.setText('On')
        elif args[0][0] == 'выключи':
            if self.bulb.turn_off() == 'ok':
                self.window.bulb_icon.setText('')
                self.window.bulb_text.setText('Off')

    @staticmethod
    def time_in_range(start, end, x):
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    def part_of_day(self):
        if self.time_in_range(dt_time(21, 0, 0), dt_time(4, 59, 59),
                              dt_time.fromisoformat(dt.now().strftime("%H:%M:%S"))):
            pod = 'Ночь'
        elif self.time_in_range(dt_time(12, 0, 0), dt_time(17, 59, 59),
                                dt_time.fromisoformat(dt.now().strftime("%H:%M:%S"))):
            pod = 'День'
        elif self.time_in_range(dt_time(18, 0, 0), dt_time(20, 59, 59),
                                dt_time.fromisoformat(dt.now().strftime("%H:%M:%S"))):
            pod = 'Вечер'
        elif self.time_in_range(dt_time(5, 0, 0), dt_time(11, 59, 59),
                                dt_time.fromisoformat(dt.now().strftime("%H:%M:%S"))):
            pod = 'Утро'
        else:
            pod = 'Hz'
        return pod

    def first_start(self):
        self.speak(f'Здравствуйте, {self.owner_name}! Меня зовут {self.name}. Я управляю данной программой.')
        self.speak(f'Чтобы инициализировать систему, скажите "Люси, запусти систему!"')

    def initialisation(self):
        while True:
            self.wake_up()

    def check_system(self):
        if not os.path.exists(f'cache/{self.weather.filename}'):
            self.weather.create_file()

        if self.bulb.get_properties()['power'] == 'on':
            self.window.bulb_text.setText('On')
        else:
            self.window.bulb_text.setText('Off')

    def checking_thread(self, stop):
        schedule.every(1).hour.at(':00').do(self.window.set_current_weather, args=self.weather.create_current_dict())
        schedule.every(1).hour.at(':00').do(self.window.set_forecast, args=self.weather.near_forecast())
        schedule.every(1).day.at('00:00').do(self.window.set_date, args=self.get_date())
        schedule.every(1).day.at('08:00').do(self.weather.create_file)
        print('данные обновлены!')
        while True:
            schedule.run_pending()
            sleep(1)
            if stop():
                break


class Window(QMainWindow, Design):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)

    def closeEvent(self, event):
        assist.speak(f'До свидания, {assist.owner_name}!')
        assist.stop_process = True
        assist.thread.join()


def main():
    while True:
        assist.initialisation()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    player = Player()
    weather = Weather()
    win = Window()
    win.show()
    assist = Assistant(player, win, weather)
    thread = Thread(target=main, daemon=True)
    thread.start()
    sys.exit(app.exec_())
