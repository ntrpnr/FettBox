from enum import Enum

from stopwatch import StopwatchState
from player_module import TimeModule
import logging, sys
import asyncio


class Game:
    def __init__(self):
        self.time_modules = []
        self.finished_players = {}

    def add_player_module(self, module: TimeModule):
        module.button_callback = self.player_button_pressed
        self.time_modules.append(module)

    async def player_button_pressed(self, color, state: StopwatchState, time):
        logging.info(f"{color}: {time} - {state}")
        state = self.get_state()
        if state is GameState.WaitingForPlayers or state is GameState.Ready:
            await self.join_player(color)
        elif state is GameState.Started:
            await self.finish_player(color)

    async def join_player(self, color):
        logging.info(f"Player joined: {color}")
        player: TimeModule = list(filter(lambda x: (x.stopwatch.color is color), self.time_modules))[0]
        await player.stopwatch.reset()
    
    async def finish_player(self, color):        
        player: TimeModule = list(filter(lambda x: (x.stopwatch.color is color), self.time_modules))[0]
        await player.stopwatch.stop()
        logging.info(f"Player finished: {color} ({player.stopwatch.calculated_time})")
        self.finished_players[color] = player.stopwatch.calculated_time

    async def start_game(self):
        [await player.start() for player in self.get_players_ready()]

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
