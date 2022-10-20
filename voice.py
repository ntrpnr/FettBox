import threading
import pyttsx3
import asyncio


from music_player import MusicPlayer

class Voice:
    def __init__(self, music_player: MusicPlayer):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')       #getting details of current voice
        #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
        self.engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
        self.engine.setProperty('rate', 135) 
        self.music_player = music_player
        self.thread: threading.Thread = None

    async def speak(self, text):
       
        #while self.thread is not None and self.thread.is_alive():
        #    await asyncio.sleep(.1)

        self.thread = threading.Thread(
            target=self.__run, args=(text,), daemon=True
        ).start()
        

    def __run(self, text):
        if self.engine._inLoop:
            self.engine.endLoop()
            
        self.music_player.duck_down()

        self.engine.say(text)        
        self.engine.runAndWait()     

        if self.engine._inLoop:
            self.engine.endLoop()
        
        self.music_player.restore_volume()
