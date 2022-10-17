import asyncio
import logging, sys
from time import sleep
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

from rich.panel import Panel
from textual.widget import Widget
from rich.style import Style

class Led(Widget):
    def __init__(self, *args, color, pin, **kwargs):
        self.color = color
        self.pin = pin
        self.current_text = "•"
        self.current_style = "on black"
        super().__init__(*args, **kwargs)
    
    def render(self) -> Panel:
        return Panel(self.current_text, style=self.current_style, border_style=Style(color="black"))

    async def on(self, brightness = 100, abort=True):
        if abort:
            self.__abort()
        self.current_style = f"{self.color} on black"
        self.refresh()
        logging.debug("LED {color} on at {brightness}%".format(color = self.color, brightness = brightness))

    async def off(self, abort=True):
        if abort:
            self.__abort()
        self.current_style = f"black on black"
        self.refresh()
        logging.debug("LED {color} off".format(color = self.color))

    async def start_blink(self, ms):
        self.__abort()
        self.is_blinking = True
        while(self.is_blinking):
            await self.on(abort=False)
            await asyncio.sleep(ms/1000)
            await self.off(abort=False)
            await asyncio.sleep(ms/1000)
        logging.debug("LED {color} blink stop".format(color = self.color))

    async def start_breath(self, ms):
        raise NotImplementedError()
        self.__abort()
        await self.off()
        self.is_breathing = True
        while(self.is_breathing):
            logging.debug("LED {color} breathing in".format(color = self.color))
            self.animate()
            for i in range(0, 100):
                self.current_style = f"red on black opacity={i}"
                await asyncio.sleep(ms/100000)
            logging.debug("LED {color} breathing out".format(color = self.color))
            for i in range(100, 0):
                self.current_style = f"red on black opacity={i}"
                await asyncio.sleep(ms/100000)
        logging.debug("LED {color} stopped breathing".format(color = self.color))

    def __abort(self):
        self.is_blinking = False
        self.is_breathing = False


