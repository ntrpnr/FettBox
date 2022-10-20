import threading
import pyttsx3
import asyncio


from music_player import MusicPlayer

class Voice:
    def __init__(self, music_player: MusicPlayer):        
        self.music_player = music_player
        self.thread: threading.Thread = None
        self.lock = threading.Lock()

    async def speak(self, text):
       
        self.thread = threading.Thread(
            target=self.__run, args=(text,), daemon=True
        ).start()
        

    def __run(self, text):
        self.lock.acquire()

        #Workaround: Re-initialize each time
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')       #getting details of current voice
        #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
        engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
        engine.setProperty('rate', 135)
            
        self.music_player.duck_down()       
        
        engine.say(text)
        engine.runAndWait()
        
        self.music_player.restore_volume()
        self.lock.release()
        
