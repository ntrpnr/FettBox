from led_button import ButtonPressed, LedButton
from textual.app import App
import logging, sys
from textual.views import GridView
import asyncio
from stopwatch import StopwatchState
logging.basicConfig(filename="log.txt", level=logging.INFO)

from time_module import TimeModule

class FettBox(App):

    async def on_mount(self) -> None:
        
        red_panel = TimeModule("red_panel", "red", led_pin=5, button_pin=4, event_callback=self.time_module_callback)
        blue_panel = TimeModule("blue_panel", "blue", led_pin=5, button_pin=4)
        green_panel = TimeModule("green_panel", "green", led_pin=5, button_pin=4)
        yellow_panel = TimeModule("yellow_panel", "yellow", led_pin=5, button_pin=4)
        white_panel = TimeModule("white_panel", "white", led_pin=5, button_pin=4)
        self.time_modules = [red_panel, blue_panel, green_panel, yellow_panel, white_panel]

        top_grid = TopGrid(*self.time_modules)

        self.start_button = LedButton("start_button", "white", 6, "START", event_callback=self.start_button_callback)
        await self.start_button.on()
        
        await self.view.dock(top_grid, self.start_button, edge="top")
        #await self.view.dock(s, edge="top")

    async def time_module_callback(self, color, state: StopwatchState, time):
        logging.info(f"{color}: {time} - {state}")

    async def start_button_callback(self):
        logging.info(f"Start button pressed")
        players = list(filter(lambda x: (x.stopwatch.state == StopwatchState.Reset), self.time_modules))
        if any(players):
            logging.info(f"Can start: {players}")
        else:
            logging.info("Can not start")


class TopGrid(GridView):
    def __init__(self, *panels):
        self.panels = panels
        self.name = "top_grid"
        super().__init__(name = self.name)

    async def on_mount(self):
        self.grid.add_column("column", repeat=5, fraction=1)
        self.grid.add_row("row", repeat=1, size=5)
        self.grid.place(*self.panels)



FettBox.run(title="Fett Box", log="textual.log")