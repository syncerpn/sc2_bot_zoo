# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 18:54:58 2022

@author: nghia_sv
"""

import random

from sc2.bot_ai import BotAI
from sc2.data import Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId

class SyncerZergMacro(BotAI):
    def __init__(self):
        self.name = 'SyncerZergMacroBot'
        self.possible_race = [Race.Zerg]
        self.glhf = '(drone)(drone)(drone)(drone)(glhf)'
        self.build_step = 0
        
        self.s_main_hatch = None
        self.s_nat_hatch = None
        self.u_nat_hatch_drone = None
        self.l_nat_hatch = None
        self.l_pool = None
        self.u_first_gas_drone = None
        self.u_pool_drone = None
        self.l_first_gas = None
        self.u_larva_consumed_tag = []

    async def on_step(self, iteration):
        if iteration == 0:
            await self.chat_send(self.glhf)
            self.s_main_hatch = self.townhalls[0]

        if self.build_step == 0:
            if self.can_afford(UnitTypeId.DRONE) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
                    self.build_step = 1
        
        if self.build_step == 1:
            if self.can_afford(UnitTypeId.OVERLORD) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_OVERLORD, subtract_cost=True, subtract_supply=True)
                    self.build_step = 2
        
        if self.build_step == 2:
            if self.can_afford(UnitTypeId.DRONE) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
                    self.build_step = 3
        
        if self.build_step == 3:
            if self.can_afford(UnitTypeId.DRONE) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
                    self.build_step = 4
        
        if self.build_step == 4:
            if self.can_afford(UnitTypeId.DRONE) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
                    self.build_step = 5
        
        if self.build_step == 5:
            if self.minerals >= 190:
                self.u_nat_hatch_drone = self.workers.random
                min_distance = 99999
                for loc in self.expansion_locations:
                    distance = loc.distance_to(self.start_location)
                    if distance == 0:
                        print('main base; skipped')
                        continue
                    if distance < min_distance:
                        min_distance = distance
                        self.l_nat_hatch = loc
                
                if self.l_nat_hatch:
                    self.u_nat_hatch_drone.smart(self.l_nat_hatch)
                    self.build_step = 6
        
        if self.build_step == 6:
            if self.can_afford(UnitTypeId.HATCHERY):
                self.u_nat_hatch_drone.build(UnitTypeId.HATCHERY, self.l_nat_hatch)
                for t in self.townhalls:
                    if t.tag != self.s_main_hatch.tag:
                        self.s_nat_hatch = t
                        break
                self.build_step = 7
        
        if self.build_step == 7:
            if self.can_afford(UnitTypeId.DRONE) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
                    self.build_step = 8
            
        if self.build_step == 8:
            if self.can_afford(UnitTypeId.DRONE) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva_r = selected_larva.random
                    selected_larva_r(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
                    min_distance = 99999
                    for vg in self.vespene_geyser:
                        distance = vg.distance_to(selected_larva_r)
                        if distance < min_distance:
                            min_distance = distance
                            self.l_first_gas = vg
                            
                    self.build_step = 9
                
        if self.build_step == 9:
            if self.can_afford(UnitTypeId.DRONE) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
                    self.build_step = 10
        
        if self.build_step == 10:
            if self.supply_used == 18 and self.supply_workers == 16:
                self.s_main_hatch(AbilityId.RALLY_WORKERS, target=self.s_main_hatch)
                self.build_step = 11
        
        if self.build_step == 11:
            min_distance = 99999
            for w in self.workers:
                if w.is_idle:
                    distance = self.l_first_gas.distance_to(w)
                    if distance < min_distance:
                        min_distance = distance
                        self.u_first_gas_drone = w
            
            if self.u_first_gas_drone:
                self.u_first_gas_drone.build_gas(self.l_first_gas)
                self.build_step = 12
        
        if self.build_step == 12:
            for w in self.workers:
                if w.is_idle and w.tag != self.u_first_gas_drone.tag:
                    self.u_pool_drone = w
            
            if self.u_pool_drone:
                map_center = self.game_info.map_center
                self.l_pool = self.start_location.towards(map_center, distance=5)
                self.u_pool_drone.smart(self.l_pool)
                self.build_step = 13
        
        if self.build_step == 13:
            if self.can_afford(UnitTypeId.SPAWNINGPOOL):
                await self.build(UnitTypeId.SPAWNINGPOOL, near=self.l_pool, build_worker=self.u_pool_drone, placement_step=1)
                self.build_step = 14
        
        if self.build_step == 14:
            self.l_first_gas = self.gas_buildings[0]
            self.s_main_hatch(AbilityId.RALLY_WORKERS, target=self.l_first_gas)
            if self.can_afford(UnitTypeId.DRONE) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
                    self.build_step = 15
        
        if self.build_step == 15:
            if self.can_afford(UnitTypeId.DRONE) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
                    self.build_step = 16
        
        if self.build_step == 16:
            if self.can_afford(UnitTypeId.DRONE) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
                    self.build_step = 17
                
        if self.build_step == 17:
            if self.supply_workers == 19:
                self.s_main_hatch(AbilityId.RALLY_WORKERS, target=self.mineral_field.closest_to(self.l_nat_hatch))
                self.build_step = 18
        
        if self.build_step == 18:
            if self.can_afford(UnitTypeId.OVERLORD) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_OVERLORD, subtract_cost=True, subtract_supply=True)
                    self.build_step = 19
        
        if self.build_step == 19:
            if self.can_afford(UnitTypeId.DRONE) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
                    self.build_step = 20
        
        if self.build_step == 20:
            if len(self.townhalls) == 2 and self.structures(UnitTypeId.SPAWNINGPOOL).ready and self.minerals >= 300:
                for t in self.townhalls:
                    t.build(UnitTypeId.QUEEN)
                self.build_step = 21
                
        if self.build_step == 21:
            if self.can_afford(UnitTypeId.ZERGLING) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_ZERGLING, subtract_cost=True, subtract_supply=True)
                    self.build_step = 22
                
        if self.build_step == 22:
            if self.can_afford(UnitTypeId.ZERGLING) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_ZERGLING, subtract_cost=True, subtract_supply=True)
                    self.build_step = 23
        
        if self.build_step == 23:
            if self.can_afford(UnitTypeId.DRONE) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
                    self.build_step = 24
        
        if self.build_step == 24:
            if self.can_afford(UnitTypeId.DRONE) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
                    self.build_step = 25
        
        if self.build_step == 25:
            if self.can_afford(UnitTypeId.DRONE) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
                    self.build_step = 26
        
        if self.build_step == 26:
            if self.can_afford(UnitTypeId.DRONE) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
                    self.build_step = 27
        
        if self.build_step == 27:
            if self.can_afford(UnitTypeId.DRONE) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
                    self.build_step = 28
        
        if self.build_step == 28:
            if self.can_afford(UnitTypeId.DRONE) and self.larva:
                selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
                if selected_larva:
                    selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
                    self.build_step = 29