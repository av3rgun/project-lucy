import vlc
from fuzzywuzzy import fuzz
from datetime import datetime as dt


class Player:
    def __init__(self):
        self.instance = vlc.Instance()
        self.instance.log_unset()
        self.player = self.instance.media_player_new()

    def select_station(self, station):
        stations = {
            "Европа Плюс": 'https://str.pcradio.ru/europa_plus-hi',
            "Energy": 'https://str.pcradio.ru/energyfm_ru-hi',
            'record': 'https://str.pcradio.ru/radiorecord_ru-hi',
            'Максимум': 'https://str.pcradio.ru/fm_maximum-hi',
            'Капитал': 'https://str.pcradio.ru/capitalfm_moscow-hi'
        }
        for s_name, s_url in stations.items():
            if fuzz.ratio(station, s_name) > 60:
                self.player.set_mrl(s_url)

    def select_channel(self, channel):
        start_time = round(dt(dt.now().year, dt.now().month, dt.now().day, dt.now().hour).timestamp())
        channels = {
            'fox': 'http://89.104.114.26:8080/fox_hd/tracks-v1a1/mono.m3u8',
            'тнт4': f'https://a775798156-s91412.cdn.ngenix.net/mdrm/CH_TNT4/bw2000000/playlist.m3u8?utcstart='
                    f'{start_time}&version=2'
        }
        for c_name, c_url in channels.items():
            if fuzz.ratio(channel, c_name) > 60:
                self.player.set_mrl(c_url)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def get_volume(self):
        return self.player.audio_get_volume()

    def set_volume(self, vol):
        return self.player.audio_set_volume(vol)
