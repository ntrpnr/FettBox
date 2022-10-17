from led_button import ButtonPressed, LedButton
from textual.app import App
from textual.widgets import Placeholder
import asyncio

from time_module import TimeModule

class FettBox(App):

    async def on_mount(self) -> None:
        self.red_panel = TimeModule("red_panel", "red", 5, 4)
        await self.view.dock(self.red_panel, edge="top")

FettBox.run(title="Fett Box", log="textual.log")