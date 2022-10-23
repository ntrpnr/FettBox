from ast import Call
import sys
import threading
from PyQt5.QtCore import pyqtSignal, Qt, QThread, qInstallMessageHandler
from PyQt5.QtGui    import QMovie
from PyQt5.QtWidgets import QApplication, QSplashScreen, QMainWindow
from typing import Callable
import asyncio

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

class SplashScreen(QSplashScreen):
    def __init__(self, filepath, callback:Callable, flags=0):
        super().__init__(flags=Qt.WindowFlags(flags))
        self.movie = QMovie(filepath, parent=self)
        self.callback = callback
        self.movie.frameChanged.connect(self.handleFrameChange)
        self.movie.start()

    def handleFrameChange(self):
        pixmap = self.movie.currentPixmap()
        self.setPixmap(pixmap)
        self.setMask(pixmap.mask())
        if self.movie.currentFrameNumber() == self.movie.frameCount()-1:
            try:
                self.movie.stop()
                self.close()
                if self.callback is not None:
                    self.callback()
            except Exception:
                pass


class Media:
    StartSequence = 'media/F1_start_light_sequence_animation.gif'

class Display:
    def __init__(self):
        self.thread: threading.Thread = None

        def handler(msg_type, msg_log_context, msg_string):
            pass

        qInstallMessageHandler(handler)

    def show(self, media: Media, callback:Callable=None):

        self.thread = threading.Thread(
            target=self.__show, args=(media,callback), daemon=True
        ).start()

    def __show(self, media, callback:Callable):
        app = QApplication(sys.argv)
        splash = SplashScreen(media, callback, Qt.WindowStaysOnTopHint)
        splash.show()
        app.exec_()



        