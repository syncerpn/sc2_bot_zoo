# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 19:06:39 2022

@author: nghia_sv
"""

import random

from sc2 import maps
from sc2.data import Difficulty, Race
from sc2.player import Bot, Computer
from sc2.main import run_game

#syncer's custom bots
from SyncerZergMacro import SyncerZergMacro

#bot spec
player = SyncerZergMacro()
player_race = random.choice(player.possible_race)
player_name = player.name

#computer spec
computer_race = Race.Protoss
computer_difficult = Difficulty.VeryHard


#fight!
run_game(
    maps.get("AcropolisLE"),
    [Bot(player_race, player, name=player_name), Computer(computer_race, computer_difficult)],
    realtime=True,
    )