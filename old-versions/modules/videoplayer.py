import vlc
from fuzzywuzzy import fuzz
from datetime import datetime as dt


class VideoPlayer:
    def __init__(self):
        self.instance = vlc.Instance('--verbose 1'.split())
        self.instance.log_unset()
        self.vplayer = self.instance.media_player_new()

    def select_channel(self, channel):
        start_time = round(dt(dt.now().year, dt.now().month, dt.now().day, dt.now().hour).timestamp())
        channels = {
            'fox': 'http://89.104.114.26:8080/fox_hd/tracks-v1a1/mono.m3u8',
            'тнт4': f'https://a775798156-s91412.cdn.ngenix.net/mdrm/CH_TNT4/bw2000000/playlist.m3u8?utcstart='
                    f'{start_time}&version=2'
        }
        for c_name, c_url in channels.items():
            if fuzz.ratio(channel, c_name) > 60:
                self.vplayer.set_mrl(c_url)

    def play(self):
        self.vplayer.play()

    def pause(self):
        self.vplayer.pause()

    def stop(self):
        self.vplayer.stop()

    def get_volume(self):
        return self.vplayer.audio_get_volume()

    def set_volume(self, vol):
        return self.vplayer.audio_set_volume(vol)

