import wave
from vosk import Model, KaldiRecognizer, SetLogLevel
import json
import pyaudio
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
from random import choice
import winsound
from colorama import Fore
from yeelight import Bulb
from time import sleep
import os
import sys


class Assistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.alias = ("люси", "люся", "луси", "лисун", "люсяш", "люська")
        self.text = ''
        self.num_task = 0
        self.j = 0
        self.answer = ''
        self.commands = [
            'привет', 'приветствую', 'хэллоу', 'добрый день'
        ]
        self.cmds = {
            ('привет', 'здарово', 'здорово', 'здравствуй'): self.hello,
            ('как дела', 'как ты', 'как сама', 'что нового'): self.doings,
            ('выключи свет', 'погаси свет', 'выруби свет'): self.bulb_off,
            ('включи свет', 'вруби свет', 'проведи свет'): self.bulb_on,
            ('яркость', 'измени яркость на', 'поменяй яркость на', 'установи яркость на'): self.change_brightness,
            ('стоп', 'stop'): self.quit
        }
        self.bulb = Bulb('192.168.0.104')
        self.logging = SetLogLevel(-1)

    def cleaner(self, text):
        self.text = text
        for alias in self.alias:
            self.text = self.text.replace(alias, '').strip()
            self.text = self.text.replace('  ', '').strip()
        self.answer = self.text

        for com in range(len(self.commands)):
            k = fuzz.ratio(text, self.commands[com])
            if (k > 70) & (k > self.j):
                self.answer = self.commands[com]
                self.j = k
        return str(self.answer)

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

    def recognizer(self, *args: list):
        with sr.Microphone() as micro:
            recognize = sr.Recognizer()
            recognize.adjust_for_ambient_noise(micro, 2)
            try:
                print("Listening..")
                audio = recognize.listen(micro, 5, 5)
                with open('cache/last-recognized.wav', 'wb') as file:
                    file.write(audio.get_wav_data())

            except sr.WaitTimeoutError:
                self.talk("Проверьте свой микрофон. Возможно он не распознаётся!")
                return

            try:
                self.text = recognize.recognize_google(audio, language='ru-RU').lower()
                if self.text.startswith(self.alias):
                    self.response()
                    self.text = self.cleaner(self.text)
                    print(Fore.GREEN + f'Вы сказали: {self.text}')
                    for tasks in self.cmds:
                        for task in tasks:
                            option = self.text.replace(task, '').strip()
                            if option != self.text:
                                self.text.replace(option, '').strip()
                                if fuzz.ratio(task, self.text.replace(option, '').strip()) >= 98:
                                    command_option = option.split(' ')
                                    self.cmds[tasks](command_option)

            except sr.UnknownValueError:
                self.talk('Простите, не могли бы вы повторить?')

            except sr.RequestError:
                print('Using offline recognition..')
                self.text = self.offline_recognition()

            return self.text

    def change_brightness(self, *args: list):
        bright = args[0]
        perc = int(bright[0].replace('%', ''))
        self.bulb.set_brightness(perc)

    def hello(self, *args: str):
        self.talk(choice(['Привет!', 'Приветствую!', 'Здравствуйте!', 'Добро пожаловать на борт!']))

    def doings(self, *args: list):
        response = [
            'А тому ли я дала?', 'Дела у прокурора, а у нас делишки', 'Как в сценарии - развязка близко',
            'Ты действительно хочешь знать или просто поговорить не о чем?', 'Смотря в каком измерении.',
            'Скажу хорошо — не поверишь, плохо — не поможешь', 'Лучше всех. Хорошо, что никто не завидует.',
            'C точки зрения банальной эрудиции игнорирую критерии утопического субъективизма, концептуально '
            'интерпретируя общепринятые дефанизирующие поляризаторы, поэтому консенсус, достигнутый диалектической '
            'материальной классификацией всеобщих мотиваций в парадогматических связях предикатов, решает проблему '
            'усовершенствования формирующих геотрансплантационных квазипузлистатов всех кинетически коррелирующих '
            'аспектов, а так нормально'
        ]
        self.talk(choice(response))

    def bulb_off(self, *args: list):
        self.bulb.turn_off()
        response = [
            'Выключаю', 'Окей', 'Хорошо', 'Будет сделано!', 'Так точно!'
        ]
        self.talk(choice(response))

    def bulb_on(self, *args: list):
        self.bulb.turn_on()
        response = [
            'Включаю', 'Окей', 'Хорошо', 'Будет сделано!', 'Так точно!'
        ]
        self.talk(choice(response))

    def talk(self, text):
        print(Fore.CYAN + f'[EVA]: {text}')
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        recogn = sr.Recognizer()
        recogn.pause_threshold = 0.5
        try:
            with sr.Microphone() as mic:
                print("Я вас слушаю..")
                recogn.adjust_for_ambient_noise(source=mic, duration=0.5)
                audio = recogn.listen(source=mic)
                self.text = recogn.recognize_google(audio_data=audio, language='ru-RU').lower()
                print(f'Вы сказали: {self.text}')
            return self.text
        except sr.UnknownValueError as _ex:
            return f'[INFO]: Ошибка\n{_ex}'

    @staticmethod
    def quit(*args: list):
        sleep(3)
        sys.exit(1)

    @staticmethod
    def response():
        file = '../Voice_Assistant MK III/sounds/response.wav'
        winsound.PlaySound(file, winsound.SND_FILENAME | winsound.SND_ASYNC)


if __name__ == '__main__':
    while True:
        Assistant().recognizer()