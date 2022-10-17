from cgitb import reset
from textual.widget import Widget
from rich.style import Style
from rich.panel import Panel
import asyncio
from textual.views import GridView

from led_button import ButtonPressed, LedButton
from stopwatch import Stopwatch, StopwatchState

class TimeModule(GridView):
    def __init__(self, name: str, color, led_pin, button_pin):
        self.name = name
        self.color = color
        self.led_pin = led_pin
        self.button_pin = button_pin        
        super().__init__(name = name)

    async def on_mount(self) -> None:
        self.led_button = LedButton(name=f"{self.color}_button", color=self.color, pin=self.led_pin)
        self.stopwatch = Stopwatch(name=f"{self.color}_stopwatch", color=self.color, pin=3)
        
        self.grid.add_column("column", repeat=2, size=8)
        self.grid.add_row("row", repeat=1, size=5)

        self.grid.add_widget(self.led_button)
        self.grid.add_widget(self.stopwatch)
        self.grid.add_areas()

        asyncio.create_task(self.start())

    # def render(self) -> Panel:
    #     return Panel(self.led_button, border_style=Style(color=self.color))

    async def handle_button_pressed(self, message: ButtonPressed) -> None:
        assert isinstance(message.sender, LedButton)
        if self.stopwatch.state == StopwatchState.Off:
            await self.stopwatch.reset()
        elif self.stopwatch.state == StopwatchState.Reset:
            await self.stopwatch.start()
        elif self.stopwatch.state == StopwatchState.Started:
            await self.stopwatch.stop()
        elif self.stopwatch.state == StopwatchState.Stopped:
            await self.stopwatch.reset()

    async def start(self):
        task = asyncio.create_task(self.led_button.start_blink(500))
        await asyncio.sleep(2)
        task.cancel()
        await self.led_button.on()

        # task = asyncio.create_task(self.led_button.start_breath(200))
        # await asyncio.sleep(2)
        # task.cancel()

        # await led.on(80)
        # await asyncio.sleep(2)
        # await led.off()