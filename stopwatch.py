import asyncio
import logging, sys
import time
from enum import Enum
#from datetime import datetime
from rich.align import Align
from timeit import repeat
from textual.widget import Widget
from rich.text import Text
from rich.padding import Padding
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class Stopwatch(Widget):
    def __init__(self, name, color, pin):
        self.name = name
        self.color = color
        self.pin = pin
        self.calculated_time = "00:00:00"
        self.current_style = f"{self.color} on black"
        self.start_time = time.time_ns()
        self.state = StopwatchState.Off
        super().__init__(name = name)

    def on_mount(self):
        self.state = StopwatchState.Off
        self.set_interval(.1234, self.refresh)

    def render(self):
        if self.state == StopwatchState.Off:
            display = ""
        elif self.state == StopwatchState.Reset:
            display = "00:00:00"
        elif self.state == StopwatchState.Stopped:
            display = self.calculated_time
        else:
            display = self.time_convert(time.time_ns() - self.start_time)
        
        text = Text(display, style=f"{self.color} on black")
        #return Padding(Align.left(text, vertical="middle"), (1,0), style=self.style)

        return Padding(
            Align.left(text, vertical="top"),
            (1, 1),
            style=f"{self.color} on black",
        )

    def time_convert(self, ns):
        hundredths = ns // 10000000
        sec = int(hundredths // 100)
        mins = int(sec // 60)
        sec = int(sec % 60)
        hundredths = int(hundredths % 100)
        mins = (mins % 60)
        return f"{mins:02}:{sec:02}:{hundredths:02}"
    
    async def reset(self):        
        self.start_time = time.time_ns()
        self.stop_time = self.start_time
        self.state = StopwatchState.Reset
        logging.debug("{color} stopwatch was reset".format(color = self.color))

    async def off(self):
        self.start_time = time.time_ns()
        self.stop_time = self.start_time()
        self.state = StopwatchState.Off
        logging.debug("{color} stopwatch is off".format(color = self.color))

    async def start(self):
        self.start_time = time.time_ns()
        self.state = StopwatchState.Started
        logging.debug("{color} stopwatch started".format(color = self.color))

    async def stop(self):
        self.stop_time = time.time_ns()
        self.calculated_time = self.time_convert(self.stop_time - self.start_time)
        self.state = StopwatchState.Stopped
        logging.debug("{color} stopwatch started".format(color = self.color))

    async def blink(self, ms):
        logging.debug("{color} stopwatch blinking".format(color = self.color))  

class StopwatchState(Enum):
    Off = 0,
    Reset = 1,
    Started = 2,
    Stopped = 3
