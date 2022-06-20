from datetime import datetime as dt, time as dt_time, timedelta as delta
from deepl import translate
from statistics import mean
import pandas as pd
import http.client
import requests
import json


class Weather:
    def __init__(self):
        self.ip = self.get_my_ip()
        self.lat = self.locate_me()[0]
        self.lon = self.locate_me()[1]
        self.place = self.locate_me()[2]
        self.current_url = self.create_current_url()
        self.forecast_url = self.create_forecast_url()
        self.filename = 'forecast.json'
        # self.forecast = self.create_forecast_dict()
        # self.current = self.create_current_dict()

    @staticmethod
    def get_my_ip():
        conn = http.client.HTTPConnection("ident.me")
        conn.request("GET", '/')
        ip = conn.getresponse().read().decode('utf-8')
        conn.close()
        return ip

    def locate_me(self):
        try:
            resp = requests.get(url=f'http://ip-api.com/json/{self.ip}')
            r = resp.json()
            lat = r['lat']
            lon = r['lon']
            place = translate('EN', 'RU', text=r['city'])
            return [lat, lon, place]
        except requests.ConnectionError as _ex:
            print(f'[Error]: {_ex}')

    def create_current_url(self):
        url = f'https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&current_weather=true' \
              f'&daily=temperature_2m_min,temperature_2m_max&timezone=Europe/Moscow'
        return url

    def create_forecast_url(self):
        url = f'https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&hourly=temperature_2m' \
              f',apparent_temperature,cloudcover,weathercode,winddirection_10m,windspeed_10m&daily=sunrise,' \
              f'sunset&timezone=Europe/Moscow'
        return url

    def create_daily_url(self):
        url = f'https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&hourly=relativehumidity_2m' \
              f'&daily=sunrise,sunset,windspeed_10m_max,precipitation_sum,winddirection_10m_dominant&timezone=Europe/Moscow'
        return url

    @staticmethod
    def time_in_range(start, end, x):
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

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

    def create_current_dict(self):
        try:
            resp = requests.get(url=self.current_url)
            r = resp.json()
            temp = r['current_weather']['temperature']
            status = r['current_weather']['weathercode']
            temp_max = r['daily']['temperature_2m_max'][0]
            temp_min = r['daily']['temperature_2m_min'][0]
            resp.close()
            current_weather_dict = {
                'current_temp': f'{round(temp)}°',
                'status_icon': self.get_status_icon(status),
                'status_text': self.get_status_text(status),
                'temp_max_min': f' {round(temp_min)}°  {round(temp_max)}°',
            }
            return current_weather_dict
        except requests.ConnectionError as _ex:
            print(f'[Error]: {_ex}')

    def create_forecast_dict(self):
        try:
            resp = requests.get(self.forecast_url)
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

    def get_avg_daily(self):
        url = self.create_daily_url()
        try:
            resp = requests.get(url)
            r = resp.json()
            resp.close()
            hours = r['hourly']['time']
            hums = r['hourly']['relativehumidity_2m']
            sunset = dt.fromisoformat(r['daily']['sunset'][0]).strftime('%H:%M')
            sunrise = dt.fromisoformat(r['daily']['sunrise'][0]).strftime('%H:%M')
            windspeed = round(r['daily']['windspeed_10m_max'][0])
            wind_dir = r['daily']['winddirection_10m_dominant'][0]
            precipitation = r['daily']['precipitation_sum'][0]
            humidity = {}
            for hour in hours:
                for hum in hums:
                    humidity.update({
                        hour: hum
                    })
            hum_list = []
            for hour, hum in humidity.items():
                dt_start = dt(dt.now().year, dt.now().month, dt.now().day, 0)
                dt_end = dt(dt.now().year, dt.now().month, dt.now().day, 23)
                if dt_start < dt.fromisoformat(hour) < dt_end:
                    hum_list.append(hum)
            return [round(mean(hum_list), 1), windspeed, self.detect_winddir(wind_dir), precipitation, sunset, sunrise]
        except requests.ConnectionError as _ex:
            print(f'[Error]: {_ex}')

    @staticmethod
    def detect_winddir(num):
        val = int((num/22.5)+.5)
        arr = ['C', 'ССВ', "СВ", "ВСВ", "В", "ВЮВ", "ЮВ", "ЮЮВ", "Ю", "ЗЗЮ", "ЗЮ", "ЗЮЗ", "З", "ЗСЗ", "СЗ", "ССЗ", "С"]
        return arr[(val % 16)]

    @staticmethod
    def get_status_text(code):
        weathercods = {
            '0': "Ясно", '1': "Ясно", '2': "Облачно", '3': "Облачно", '45': "Туман", '48': "Туман", '51': "Морось",
            '53': "Морось", '55': "Морось", '56': "Обледенение", '57': "Обледенение", '61': "Дождь", '63': "Дождь",
            '65': "Дождь", '66': "Град", '67': "Град", '71': "Снег", '73': "Снег", '75': "Метель",
            '77': "Снежные хлопья",
            '80': "Ливень", '81': "Ливень", '82': "Ливень", '85': "Снегопад", '86': "Снегопад", '95': "Гроза",
            '96': "Гроза", '99': "Гроза"
        }
        for codes, status in weathercods.items():
            if str(round(code)) == codes:
                status_text = status
                return status_text

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

    def get_status_icon(self, status):
        pod = self.what_part_of_day(dt.now().timestamp())
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
                status_icon = icons
                return status_icon

    def create_file(self):
        db = self.create_forecast_dict()
        start_time = dt(year=dt.now().year, month=dt.now().month, day=dt.now().day, hour=8).timestamp()
        end_time = (dt(year=dt.now().year, month=dt.now().month, day=dt.now().day, hour=8) + delta(
            hours=24)).timestamp()
        near = db[(db['time'] > start_time) & (db['time'] <= end_time)].set_index('time').T.to_dict()
        n_weather = []
        for time_data, weather_data in near.items():
            weather = {
                time_data: weather_data
            }
            n_weather.append(weather)
        try:
            with open(f'cache/{self.filename}', 'w', encoding='utf-8') as file:
                json.dump(n_weather, file, ensure_ascii=False, indent=4)
                print(f'[INFO]: Файл {self.filename} успешно сохранён!')
        except Exception as _ex:
            print(f'[Error]: {_ex}')

    def near_forecast(self):
        with open(f'cache/{self.filename}', 'r') as file:
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

    def set_background(self):
        pod = self.what_part_of_day(dt.now().timestamp())
        cur = self.create_current_dict()
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


if __name__ == '__main__':
    weather = Weather()
    print(weather.near_forecast())


