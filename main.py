from led_button import ButtonPressed, LedButton
from textual.app import App
from textual.widgets import Placeholder
import asyncio

from time_module import TimeModule

class FettBox(App):

    async def on_mount(self) -> None:
        self.red_panel = TimeModule("red_panel", "red", led_pin=5, button_pin=4)
        self.blue_panel = TimeModule("blue_panel", "blue", led_pin=5, button_pin=4)
        self.green_panel = TimeModule("green_panel", "green", led_pin=5, button_pin=4)
        self.yellow_panel = TimeModule("yellow_panel", "yellow", led_pin=5, button_pin=4)
        self.white_panel = TimeModule("white_panel", "white", led_pin=5, button_pin=4)
        
        await self.view.dock(self.red_panel, self.blue_panel, self.green_panel, self.yellow_panel, self.white_panel, edge="left")

FettBox.run(title="Fett Box", log="textual.log")