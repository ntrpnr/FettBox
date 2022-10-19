import vlc

class MusicPlayer:
    def f1Theme(self):
        p = vlc.MediaPlayer("./media/f1.mp3")
        p.play()
