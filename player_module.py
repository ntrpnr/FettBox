from cgitb import reset
from typing import Any, Awaitable, Callable
from textual.widget import Widget
from rich.style import Style
from rich.panel import Panel
import asyncio
from textual.views import GridView

from led_button import ButtonPressed, LedButton
from stopwatch import Stopwatch, StopwatchState
AsyncFuncType = Callable[[Any, Any], Awaitable[Any]]

class TimeModule(GridView):
    def __init__(self, name: str, color, led_pin, button_pin, button_callback: AsyncFuncType = None):
        self.name = name
        self.color = color
        self.led_pin = led_pin
        self.button_pin = button_pin
        self.button_callback = button_callback
        super().__init__(name = name)

    async def on_mount(self) -> None:
        self.led_button = LedButton(name=f"{self.color}_button", color=self.color, pin=self.led_pin)
        self.stopwatch = Stopwatch(name=f"{self.color}_stopwatch", color=self.color, pin=3)
        
        self.grid.add_column(repeat=1, fraction=1, name="led_button")
        self.grid.add_column(repeat=1, fraction=2, name="stopwatch")
        self.grid.add_row("row", repeat=1, fraction=1)

        self.grid.add_widget(self.led_button)
        self.grid.add_widget(self.stopwatch)

    async def handle_button_pressed(self, message: ButtonPressed) -> None:
        assert isinstance(message.sender, LedButton)

        if self.button_callback is not None:
            await self.button_callback(self.color, self.stopwatch.state, self.stopwatch.calculated_time)

    async def start(self):
        await self.stopwatch.start()

    async def off(self):
        await self.stopwatch.off()