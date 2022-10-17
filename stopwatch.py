import asyncio
import logging, sys
from textual.widget import Widget
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class Stopwatch(Widget):
    def __init__(self, color, pin):
        self.color = color
        self.pin = pin
    
    def reset(self):
        logging.debug("{color} stopwatch was reset".format(color = self.color))

    def off(self):
        logging.debug("{color} stopwatch is off".format(color = self.color))

    async def start(self):
        logging.debug("{color} stopwatch started".format(color = self.color))

    async def blink(self, ms):
        logging.debug("{color} stopwatch blinking".format(color = self.color))  