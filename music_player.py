from vlc import MediaPlayer
class MusicPlayer:
    def f1Theme(self):
        self.vlc: MediaPlayer = MediaPlayer("./media/f1.mp3")
        self.set_volume(100)
        self.vlc.play()
    
    def duck_down(self):
        self.vlc.audio_set_volume(60)

    def restore_volume(self):
        self.vlc.audio_set_volume(self.last_volume)

    def set_volume(self, volume):
        self.last_volume = volume
        self.vlc.audio_set_volume(volume)
