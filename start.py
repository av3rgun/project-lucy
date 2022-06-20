import threading

import requests
from PyQt5.QtWidgets import QMainWindow
from design import Ui_MainWindow as Design
from datetime import datetime as dt, time as dt_time, timedelta as delta
from deepl import translate
from PyQt5 import QtWidgets, QtGui
from threading import Thread
from time import sleep
import pandas as pd
import http.client
import schedule
import psutil
import json
import sys


class Window(QMainWindow, Design):
    def __init__(self, target_app):
        super(Window, self).__init__()
        self.setupUi(self)
        self.stop_process = False
        self.thread = Thread(target=target_app, args=(lambda: self.stop_process, ))
        self.thread.start()

    def closeEvent(self, event):
        self.stop_process = True
        self.thread.join()


def url_for_current():
    conn = http.client.HTTPConnection("ident.me")
    conn.request("GET", '/')
    ip = conn.getresponse().read().decode('utf-8')
    conn.close()
    try:
        resp = requests.get(url=f'http://ip-api.com/json/{ip}')
        r = resp.json()
        lat = r['lat']
        lon = r['lon']
        url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true' \
              f'&daily=temperature_2m_min,temperature_2m_max&timezone=Europe/Moscow'
        resp.close()
        return url
    except requests.ConnectionError as _ex:
        print(f'[Error]: {_ex}')


def get_current_data():
    try:
        resp = requests.get(url=url_for_current())
        r = resp.json()
        temp = r['current_weather']['temperature']
        status = r['current_weather']['weathercode']
        windspeed = r['current_weather']['windspeed']
        wind_dir = r['current_weather']['winddirection']
        temp_max = r['daily']['temperature_2m_max'][0]
        temp_min = r['daily']['temperature_2m_min'][0]
        resp.close()
        current_weather_dict = {
            'current_temp': f'{round(temp)}°',
            'status_icon': get_status_icon(status),
            'status_text': get_status_text(status),
            'temp_max_min': f' {round(temp_min)}°  {round(temp_max)}°',
            'wind_speed': windspeed,
            'wind_dir': wind_dir
        }
        return current_weather_dict
    except requests.ConnectionError as _ex:
        print(f'[Error]: {_ex}')


def time_in_range(start, end, x):
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


def what_part_of_day():
    if time_in_range(dt_time(21, 0, 0), dt_time(4, 59, 59),
                     dt_time.fromisoformat(dt.now().strftime("%H:%M:%S"))):
        pod = 'Ночь'
    elif time_in_range(dt_time(12, 0, 0), dt_time(17, 59, 59), dt_time.fromisoformat(dt.now().strftime("%H:%M:%S"))):
        pod = 'День'
    elif time_in_range(dt_time(18, 0, 0), dt_time(20, 59, 59), dt_time.fromisoformat(dt.now().strftime("%H:%M:%S"))):
        pod = 'Вечер'
    elif time_in_range(dt_time(5, 0, 0), dt_time(11, 59, 59), dt_time.fromisoformat(dt.now().strftime("%H:%M:%S"))):
        pod = 'Утро'
    else:
        pod = 'Hz'
    return pod


def get_status_icon(code):
    pod = what_part_of_day()
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
        if str(round(code)) == codes:
            icon = icons
            return icon


def get_status_text(code):
    weathercods = {
        '0': "Ясно", '1': "Ясно", '2': "Облачно", '3': "Облачно", '45': "Туман", '48': "Туман", '51': "Морось",
        '53': "Морось", '55': "Морось", '56': "Обледенение", '57': "Обледенение", '61': "Дождь", '63': "Дождь",
        '65': "Дождь", '66': "Град", '67': "Град", '71': "Снег", '73': "Снег", '75': "Метель", '77': "Снежные хлопья",
        '80': "Ливень", '81': "Ливень", '82': "Ливень", '85': "Снегопад", '86': "Снегопад", '95': "Гроза",
        '96': "Гроза", '99': "Гроза"
    }
    for codes, status in weathercods.items():
        if str(round(code)) == codes:
            data = status
            return data


def get_date():
    day = dt.now().day
    month = dt.now().month
    month_f = translate('EN', 'RU', text=dt.now().strftime("%B"))
    if month == 3 or month == 8:
        month_s = f'{month_f}a'
    else:
        month_s = month_f.replace(month_f[-1], 'я')
    return f'{day} {month_s}'


def get_place():
    conn = http.client.HTTPConnection("ident.me")
    conn.request("GET", '/')
    ip = conn.getresponse().read().decode('utf-8')
    conn.close()
    try:
        resp = requests.get(url=f'http://ip-api.com/json/{ip}')
        r = resp.json()
        place = translate('EN', 'RU', text=r['city'])
        resp.close()
        return place
    except requests.ConnectionError as _ex:
        print(f'[Error]: {_ex}')


def url_for_forecast():
    conn = http.client.HTTPConnection("ident.me")
    conn.request("GET", '/')
    ip = conn.getresponse().read().decode('utf-8')
    conn.close()
    try:
        resp = requests.get(url=f'http://ip-api.com/json/{ip}')
        r = resp.json()
        lat = r['lat']
        lon = r['lon']
        url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m' \
              f',apparent_temperature,cloudcover,weathercode,winddirection_10m,windspeed_10m&daily=sunrise,' \
              f'sunset&timezone=Europe/Moscow'
        resp.close()
        return url
    except requests.ConnectionError as _ex:
        print(f'[Error]: {_ex}')


def get_forecast_data():
    url = url_for_forecast()
    try:
        resp = requests.get(url)
        r = resp.json()
        resp.close()
        time_db = r['hourly']['time']
        temp_db = r['hourly']['temperature_2m']
        apparent_db = r['hourly']['apparent_temperature']
        clouds_db = r['hourly']['cloudcover']
        wind_speed_db = r['hourly']['windspeed_10m']
        status_db = r['hourly']['weathercode']
        wind_dir_db = r['hourly']['winddirection_10m']
        stamp = []
        for el in time_db:
            stamp.append(dt.fromisoformat(str(el)).timestamp())
        data = pd.DataFrame({
            "time": stamp,
            "temp": temp_db,
            "apparent": apparent_db,
            "clouds": clouds_db,
            "wind_speed": wind_speed_db,
            "wind_dir": wind_dir_db,
            "status": status_db
        })
        return data
    except requests.ConnectionError as _ex:
        print(f'[Error]: {_ex}')


def create_file():
    db = get_forecast_data()
    start_time = dt(year=dt.now().year, month=dt.now().month, day=dt.now().day, hour=8).timestamp()
    end_time = (dt(year=dt.now().year, month=dt.now().month, day=dt.now().day, hour=8) + delta(hours=24)).timestamp()
    near = db[(db['time'] > start_time) & (db['time'] <= end_time)].set_index('time').T.to_dict()
    n_weather = []
    for time_data, weather_data in near.items():
        weather = {
            time_data: weather_data
        }
        n_weather.append(weather)
    try:
        filename = 'forecast.json'
        with open(f'data/{filename}', 'w', encoding='utf-8') as file:
            json.dump(n_weather, file, ensure_ascii=True, indent=4)
            print(f'[INFO]: Файл {filename} успешно сохранён!')
    except Exception as _ex:
        print(f'[Error]: {_ex}')


def get_near_forecast():
    with open('data/forecast.json', 'r') as file:
        forecast = json.load(file)
    output = []
    for row in forecast:
        for stamp, data in row.items():
            if round(dt.now().timestamp()) <= round(float(stamp)) <= round((dt.now() + delta(hours=6)).timestamp()):
                forecast_row = {
                    round(float(stamp)): data
                }
                output.append(forecast_row)
    return output


def get_bg():
    pod = what_part_of_day()
    cur = get_current_data()
    if pod == 'День' and cur['status_text'] == 'Ливень':
        picture = 'rainy-day'
    elif pod == 'Вечер' and cur['status_text'] == 'Ливень':
        picture = 'rainy-evening'
    elif pod == 'Вечер' and cur['status_text'] == 'Облачно':
        picture = 'cloudy-evening'
    elif pod == 'Вечер' and cur['status_text'] == 'Ясно':
        picture = 'sunny-evening'
    elif pod == 'Ночь' and cur['status_text'] == 'Ясно' and float(cur['current_temp'].replace('°', '')) > 20:
        picture = 'warm-clear-night'
    elif pod == 'Ночь' and cur['status_text'] == 'Ясно' and float(cur['current_temp'].replace('°', '')) < 20:
        picture = 'cold-clear-night'
    elif pod == 'Утро' and cur['status_text'] == 'Ясно' and float(cur['current_temp'].replace('°', '')) > 20:
        picture = 'warm-sunny-morning'
    elif pod == 'Утро' and cur['status_text'] == 'Ясно' and float(cur['current_temp'].replace('°', '')) < 20:
        picture = 'cold-sunny-morning'
    else:
        picture = 'sunny-day'
    return picture


def perc_of_used_memory():
    proc = psutil.Process()
    all_memory = psutil.virtual_memory()[0]
    used = proc.memory_info()[0]
    percentage = round((used * 100) / all_memory, 1)
    return percentage


def perc_of_used_cpu():
    cpu = psutil.Process()
    times = 1
    cpu_data = []
    while times < 3:
        cpu_data.append(cpu.cpu_percent(interval=None))
        sleep(1)
        times += 1
    return cpu_data[-1]


def update_current_weather():
    win.set_current_weather(get_current_data())
    print('Погода обновлена!')


def update_forecast():
    win.set_forecast(get_near_forecast())
    print('Прогноз обновлен!')


def update_date():
    win.set_date(get_date())
    print('Дата обновлена!')


def update_ram_usage():
    win.set_ram_usage(perc_of_used_memory())


def update_cpu_usage():
    win.set_cpu_usage(perc_of_used_cpu())


def run(stop):
    schedule.every(1).hour.at(':00').do(update_current_weather)
    schedule.every(1).minute.at(':00').do(update_ram_usage)
    schedule.every(1).minute.at(':00').do(update_cpu_usage)
    schedule.every(1).hour.at(':00').do(update_forecast)
    schedule.every(1).day.at('00:00').do(update_date)
    schedule.every(1).day.at('08:00').do(create_file)

    while True:
        schedule.run_pending()
        sleep(1)
        if stop():
            break


def main():
    win.generate_bg(get_bg())
    win.set_date(get_date())
    win.set_current_weather(get_current_data())
    win.set_forecast(get_near_forecast())
    win.set_cpu_usage(perc_of_used_cpu())
    win.set_ram_usage(perc_of_used_memory())
    win.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Window(run)
    main()
    sys.exit(app.exec_())