from textual.widget import Widget
from rich.style import Style
from rich.panel import Panel
import asyncio
from textual.views import GridView

from led_button import ButtonPressed, LedButton

class TimeModule(GridView):
    def __init__(self, name: str, color, led_pin, button_pin):
        self.name = name
        self.color = color
        self.led_pin = led_pin
        self.button_pin = button_pin
        self.led_button = LedButton(name=f"{color}_button", color=color, pin=led_pin)
        super().__init__(name = name)

    async def on_mount(self) -> None:
        self.led_button = LedButton(name=f"{self.color}_button", color=self.color, pin=self.led_pin)

        self.grid.add_column("column", repeat=2, size=40)
        self.grid.add_row("row", repeat=1, size=40)
        self.grid.add_widget(self.led_button)
        asyncio.create_task(self.start())

    def render(self) -> Panel:
        return Panel(self.led_button, border_style=Style(color="black"))

    async def handle_button_pressed(self, message: ButtonPressed) -> None:
        assert isinstance(message.sender, LedButton)
        await self.led_button.set_color("green")

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