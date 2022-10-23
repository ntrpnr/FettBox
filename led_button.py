import asyncio
import logging, sys
import threading
from time import sleep
from typing import Any, Awaitable, Callable
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

from rich.panel import Panel
from rich.align import Align
from rich.console import Console, ConsoleOptions, RenderResult, RenderableType
from rich.style import Style, StyleType

from textual.widget import Widget
from textual import events
from textual.message import Message
from textual.reactive import Reactive
from rich.padding import Padding
AsyncFuncType = Callable[[Any, Any], Awaitable[Any]]

class ButtonPressed(Message, bubble=True):
    pass

class ButtonRenderable:
    def __init__(self, label: RenderableType, style: StyleType = "") -> None:
        self.label = label
        self.style = style

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        #width = options.max_width
        #height = options.height or 1

        yield Padding(
            Align.right(self.label, vertical="top"),
            (1, 1),
            style=self.style,
        )

        # return Padding(
        #     Align.right(
        #         self.label, vertical="middle"
        #     ), (0,1), style=self.style
        # )

class LedButton(Widget):
    def __init__(self, name: str, color, pin, label =  "⬤", button_callback: AsyncFuncType = None):
        self.name = name
        self.label =  label
        self.color = color
        self.pin = pin
        self.is_breathing = False
        self.is_blinking = False
        self.thread = threading.Thread()
        self.event_callback = button_callback
        self.current_style = f"black on black"
        super().__init__(name = name)
    
    # def render(self) -> Panel:
    #     return Panel(self.current_text, style=self.current_style, border_style=Style(color="black"))

    def render(self) -> RenderableType:
        return ButtonRenderable(self.label, style=self.current_style)

    async def on_click(self, event: events.Click) -> None:
        event.prevent_default().stop()
        if self.event_callback is not None:
            await self.event_callback()
        await self.emit(ButtonPressed(self))

    async def on(self, brightness = 100, abort=True):
        if abort:
            task = asyncio.create_task(self.__abort())
            await task
        self.current_style = f"{self.color} on black"
        self.refresh()
        logging.debug("LED {color} on at {brightness}%".format(color = self.color, brightness = brightness))

    async def set_color(self, color):
        self.color = color
        self.current_style = f"{self.color} on black"
        self.refresh()

    async def off(self, abort=True):
        if abort:
            await self.__abort()
        self.current_style = f"black on black"
        self.refresh()
        logging.debug("LED {color} off".format(color = self.color))

    async def start_blink(self, ms):
        await self.__abort()
        self.is_blinking = True

        self.thread = threading.Thread(
            target=asyncio.run, args=(self.__start_blink(ms),), daemon=True
        ).start()
        
        #logging.debug("LED {color} blink stop".format(color = self.color))

    async def __start_blink(self, ms):
        while(self.is_blinking):
            await self.on(abort=False)
            await asyncio.sleep(ms/1000)
            await self.off(abort=False)
            await asyncio.sleep(ms/1000)

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

    async def __abort(self):
        if self.is_blinking or self.is_breathing:
            self.is_blinking = False
            self.is_breathing = False
            if self.thread is not None and self.thread.is_alive():
                self.thread.join()
            self.refresh()
            await asyncio.sleep(.501)
            logging.debug("Abort {color} finihsed".format(color = self.color))


