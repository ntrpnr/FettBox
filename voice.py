import threading
import pyttsx3
import asyncio

class Voice:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')       #getting details of current voice
        #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
        self.engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
        self.engine.setProperty('rate', 135) 

    async def speak(self, text):
        threading.Thread(
            target=self.__run, args=(text,), daemon=True
        ).start()
        

    def __run(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
