from ast import Call
from multiprocessing.resource_sharer import stop
import time
import threading
from typing import Callable
from vlc import MediaPlayer
import asyncio

class MusicPlayer:
    def __init__(self):
        self.is_fading = False
        self.thread: threading.Thread = None

    def f1Theme(self):
        self.__abort()
        self.vlc: MediaPlayer = MediaPlayer("./media/f1.mp3")
        self.set_volume(100)
        self.vlc.play()

    def f1ThemeStart(self):
        self.__abort()
        self.vlc: MediaPlayer = MediaPlayer("./media/f1-start.mp3")
        self.set_volume(100)
        self.vlc.play()
    
    def duck_down(self):
        if self.is_fading is False:
            self.vlc.audio_set_volume(60)

    def restore_volume(self):
        if self.is_fading is False:
            self.vlc.audio_set_volume(self.last_volume)

    def set_volume(self, volume, abort = True):
        if(abort):
            self.__abort()
        self.last_volume = volume
        self.vlc.audio_set_volume(volume)

    def fade(self, target=0, fade_time_ms=1000, fade_callback: Callable = None, stop_music = False):
        assert(target >= 0 and target <= 100)
        sleep_time_s = (fade_time_ms / abs(target - self.vlc.audio_get_volume())) / 1000
        self.thread = threading.Thread(
            target=self.__fade, args=(target,sleep_time_s, self.set_volume, fade_callback, stop_music), daemon=True
        ).start()

    def __fade(self, target, sleep_time_s, set_volume: Callable, fade_callback: Callable, stop_music):        
        last_volume = self.vlc.audio_get_volume()
        self.is_fading = True
        while self.is_fading and last_volume is not target:
            if last_volume > target:
                volume = last_volume - 1
            else:
                volume = last_volume + 1
            set_volume(volume, abort = False)            
            last_volume = volume
            time.sleep(sleep_time_s)
        self.is_fading = False
        if stop_music:
            self.vlc.stop()
        fade_callback()

    def __abort(self):
        if self.is_fading:
            self.is_fading = False
            if self.thread is not None and self.thread.is_alive():
                self.thread.join()
