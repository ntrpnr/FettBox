from copyreg import dispatch_table
from display import Display, Media
from game import Game, GameState
from led_button import ButtonPressed, LedButton
from textual.app import App
import logging, sys
from textual.views import GridView
import asyncio
from music_player import MusicPlayer
from stopwatch import StopwatchState
from voice import Voice
logging.basicConfig(filename="log.txt", level=logging.INFO)

from player_module import PlayerModule

class FettBox(App):

    async def on_mount(self) -> None:
        
        self.music_player = MusicPlayer()
        self.voice = Voice(self.music_player)
        self.led_matrix = Display()        
        self.start_button = LedButton("start_button", "white", 6, "START", button_callback=self.start_button_callback)
        self.game = Game(self.voice, self.led_matrix, self.start_button)        
        self.music_player.f1Theme()
        

        self.game.add_player_module(PlayerModule("red_panel", "red", led_pin=5, button_pin=4))
        self.game.add_player_module(PlayerModule("blue_panel", "blue", led_pin=5, button_pin=4))
        self.game.add_player_module(PlayerModule("green_panel", "green", led_pin=5, button_pin=4))
        self.game.add_player_module(PlayerModule("yellow_panel", "yellow", led_pin=5, button_pin=4))
        self.game.add_player_module(PlayerModule("white_panel", "white", led_pin=5, button_pin=4))
        

        top_grid = TopGrid(*self.game.time_modules)

        await self.start_button.on()
        
        await self.view.dock(top_grid, self.start_button, edge="top")

    

    async def start_button_callback(self):
        await self.game.start_button_pressed()
        


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