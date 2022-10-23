from enum import Enum
from display import Display, Media

from stopwatch import StopwatchState
from player_module import PlayerModule
import logging, sys
import asyncio
import time

from voice import Voice


class Game:
    def __init__(self, voice: Voice, led_matrix: Display):
        self.voice = voice
        self.led_matrix = led_matrix
        self.time_modules = []
        self.lights_are_out = False
        self.finished_players = {}

    def add_player_module(self, module: PlayerModule):
        module.button_callback = self.player_button_pressed
        self.time_modules.append(module)

    async def blink_player_buttons(self):
        [await asyncio.tasks.create_task(time_module.led_button.start_blink(500)) for time_module in self.time_modules]

    async def turn_off_non_playing(self):
        [await asyncio.tasks.create_task(player.led_button.off()) for player in self.get_players_not_playing()]

    async def start_button_pressed(self):
        logging.info(f"Start button pressed")        
        if self.get_state() is GameState.WaitingForPlayers:
            await self.blink_player_buttons()
        if self.get_state() is GameState.Ready:
            await self.start_game()
        elif self.get_state() is GameState.Stopped:
            await self.reset_game()
        else:
            logging.info("Can not start")

    async def player_button_pressed(self, color, state: StopwatchState, time):
        logging.info(f"{color}: {time} - {state}")
        state = self.get_state()
        if state is GameState.WaitingForPlayers or state is GameState.Ready:
            await self.join_player(color)
        elif state is GameState.Started:
            await self.finish_player(color)

    async def join_player(self, color):
        logging.info(f"Player joined: {color}")
        await self.voice.speak(f"{color} player joined the game.")
        player: PlayerModule = list(filter(lambda x: (x.stopwatch.color is color), self.time_modules))[0]
        await player.stopwatch.reset()
        await player.led_button.on()
    
    async def finish_player(self, color):        
        player: PlayerModule = list(filter(lambda x: (x.stopwatch.color is color), self.time_modules))[0]
        await player.stopwatch.stop()
        logging.info(f"Player finished: {color} ({player.stopwatch.calculated_time})")
        self.finished_players[color] = player.stopwatch.calculated_time

    async def start_game(self):        
        asyncio.tasks.create_task(self.voice.speak("Game is starting"))
        await self.turn_off_non_playing()
        self.lights_are_out = False
        self.led_matrix.show(Media.StartSequence, callback=self.lights_out)
        while self.lights_are_out is False:
            await asyncio.sleep(.01)
        start_time = time.time_ns()
        [await player.start(start_time) for player in self.get_players_ready()]

    def lights_out(self):
        self.lights_are_out = True
        
    #async def start_formation_lap(self):


    async def reset_game(self):
        [await time_module.off() for time_module in self.time_modules]

    def get_players(self):
        return self.time_modules

    def get_players_started(self):
        return list(filter(lambda x: (x.stopwatch.state == StopwatchState.Started), self.time_modules))

    def get_players_finished(self):
        return list(filter(lambda x: (x.stopwatch.state == StopwatchState.Stopped), self.time_modules))

    def get_players_ready(self):
        return list(filter(lambda x: (x.stopwatch.state == StopwatchState.Reset), self.time_modules))

    def get_players_not_playing(self):
        return list(filter(lambda x: (x.stopwatch.state == StopwatchState.Off), self.time_modules))

    def get_state(self):
        players_started = self.get_players_started()
        if any(players_started):
            return GameState.Started

        players_finished = self.get_players_finished()
        if any(players_finished):
            return GameState.Stopped

        players_ready = self.get_players_ready()
        if any(players_ready):
            return GameState.Ready
        else:
            return GameState.WaitingForPlayers

class GameState(Enum):
    WaitingForPlayers = 0,
    Ready = 1
    Started = 2,
    Stopped = 3
