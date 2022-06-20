from vosk import Model, KaldiRecognizer, SetLogLevel
import speech_recognition as sr
from datetime import datetime as dt, time as dt_time, timedelta as delta
from fuzzywuzzy import fuzz
from colorama import Fore
from random import choice
from threading import Thread
from time import sleep
import winsound
import pyttsx3
import wave
import json
import sys
import vlc
import os


class Assistant:
    def __init__(self, player):
        self.name = 'люси'
        self.alias = (self.name, 'ляся', 'люсяш', 'люсия', 'луси', 'люська', 'люся')
        self.logging = SetLogLevel(-1)
        self.engine = pyttsx3.init()
        self.text = ''
        self.answer = ''
        self.opts = {
            "tbr": ('включи', 'выключи', 'открой', 'закрой', 'зайди', 'найди', 'сделай'),
            "cmds": {('привет', 'здравствуй', 'приветствую', 'хай', 'ну привет'): self.hello,
                     ('радио', 'radio'): self.radio,
                     ('громкость', 'звук'): self.set_volume,
                     ('канал',): self.channel,
                     ('стоп', 'stop'): self.quit
                     }
        }
        self.owner_name = 'Александр'
        self.pod = self.part_of_day()
        self.player = player
        self.action = ''
        self.option = ''

    def offline_recognition(self):
        try:
            if not os.path.exists("models/vosk-model-small-ru-0.22"):
                print(Fore.RED + "Please download the model from:\n" +
                      "https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
                exit(1)

            wave_audio = wave.open('../cache/last-recognized.wav', 'rb')
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

    def wake_up(self):
        with sr.Microphone() as micro:
            recognize = sr.Recognizer()
            recognize.adjust_for_ambient_noise(micro, 2)
            try:
                print("Listening..")
                audio = recognize.listen(micro, 2, 2)
                with open('../cache/last-recognized.wav', 'wb') as file:
                    file.write(audio.get_wav_data())

            except sr.WaitTimeoutError:
                print("Проверьте свой микрофон. Возможно он не распознаётся!")
                return

            try:
                self.text = recognize.recognize_google(audio, language='ru-RU').lower()
                if self.text in self.alias:
                    self.response()
                    self.recognize()

            except sr.UnknownValueError:
                print('Простите, не могли бы вы повторить?')

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
                with open('../cache/last-recognized.wav', 'wb') as file:
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
        file = '../sounds/response1.wav'
        winsound.PlaySound(file, winsound.SND_FILENAME | winsound.SND_ASYNC)

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
            self.player.play()
        elif args[0][0] == 'выключи':
            self.player.stop()

    def set_volume(self, *args: list):
        current_volume = self.player.get_volume()
        numbers = {
            'один': 1, 'два': 2, 'три': 3, 'четыре': 4, 'пять': 5,
            'шесть': 6, 'семь': 7, 'восемь': 8, 'девять': 9, 'десять': 10
        }
        for word, number in numbers.items():
            if args[0][1] == word:
                vol = number
                if current_volume == vol*10:
                    self.speak('Ничего не изменилось!')
                else:
                    self.player.set_volume(vol*10)

    def quit(self, *args):
        self.speak(f'До свидания {self.owner_name}!')
        sleep(2)
        sys.exit(1)

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


if __name__ == '__main__':
    while True:
        Assistant().wake_up()