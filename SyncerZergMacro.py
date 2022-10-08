# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 18:54:58 2022

@author: nghia_sv
"""

from sc2.bot_ai import BotAI
from sc2.data import Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId

from helper.UnitTracker import UnitTracker
from helper.InfoTracker import InfoTracker

larva_unittypeid_to_abilityid = {
     UnitTypeId.DRONE: AbilityId.LARVATRAIN_DRONE,
     UnitTypeId.OVERLORD: AbilityId.LARVATRAIN_OVERLORD,
     UnitTypeId.ZERGLING: AbilityId.LARVATRAIN_ZERGLING,
     UnitTypeId.ROACH: AbilityId.LARVATRAIN_ROACH,
     UnitTypeId.HYDRALISK: AbilityId.LARVATRAIN_HYDRALISK,
     UnitTypeId.MUTALISK: AbilityId.LARVATRAIN_MUTALISK,
     UnitTypeId.CORRUPTOR: AbilityId.LARVATRAIN_CORRUPTOR,
     UnitTypeId.ULTRALISK: AbilityId.LARVATRAIN_ULTRALISK,
     UnitTypeId.INFESTOR: AbilityId.LARVATRAIN_INFESTOR,
     UnitTypeId.VIPER: AbilityId.LARVATRAIN_VIPER,
     UnitTypeId.SWARMHOSTMP: AbilityId.LOCUSTTRAIN_SWARMHOST,
     UnitTypeId.QUEEN: AbilityId.TRAINQUEEN_QUEEN,
}

class SyncerZergMacro(BotAI):
    def __init__(self):
        self.name = 'SyncerZergMacroBot'
        self.possible_race = [Race.Zerg]
        self.glhf = '(drone)(drone)(drone)(drone)(glhf)'
        self.build_step = 0
        
        self.unit_tracker = UnitTracker()
        
        self.info_tracker = InfoTracker(['base_1_location',
                                         'base_1_structure',
                                         'pool_location',
                                         'gas_first',
                                         ])
    
    def random_larva_train_and_track(self, unit_type_id, name=''):
        ability_id = larva_unittypeid_to_abilityid[unit_type_id]
        if self.can_afford(unit_type_id) and self.larva:
            selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
            if selected_larva:
                self.unit_tracker.queue(unit_type_id, name)
                selected_larva.random(ability_id, subtract_cost=True, subtract_supply=True)
                return True
            
        return False
    
    def find_natural_expansion(self):
        min_distance = 99999
        for loc in self.expansion_locations:
            distance = loc.distance_to(self.start_location)
            if distance == 0:
                continue
            if distance < min_distance:
                min_distance = distance
                self.info_tracker.store('base_1_location', loc)
    
    def map_base_divide_and_conquer(self):
        print(len(self.expansion_locations))
    
    async def on_step(self, iteration):

        #tracking every step: add tag to tracker and remove unavailable tags
        self.unit_tracker.update(self.all_units)
        # print(self.all_units)
        print(f'[INFO] {iteration} : UnitTracker\n{self.unit_tracker}')
        #tracking end
        
        if iteration == 0:
            await self.chat_send(self.glhf)
            self.unit_tracker.rename('base_0', prev_name='', amount=1, unit_type_id=UnitTypeId.HATCHERY)
            selected = self.unit_tracker.rename('scout_overlord_enemy_main', prev_name='', amount=0, unit_type_id=UnitTypeId.OVERLORD)
            self.find_natural_expansion()
            
            self.map_base_divide_and_conquer()
            
            #BO: send the first overlord to scout enemy main
            if selected:
                u = self.all_units.by_tag(selected[0])
                u.smart(self.enemy_start_locations[0])

        #BO: drone 13
        if self.build_step == 0:
            if self.random_larva_train_and_track(UnitTypeId.DRONE): self.build_step += 1
        
        if self.build_step == 1:
            if self.random_larva_train_and_track(UnitTypeId.OVERLORD): self.build_step += 1
        
        if self.build_step == 2:
            if self.random_larva_train_and_track(UnitTypeId.DRONE): self.build_step += 1
            
        if self.build_step == 3:
            if self.random_larva_train_and_track(UnitTypeId.DRONE): self.build_step += 1
            
        if self.build_step == 4:
            if self.random_larva_train_and_track(UnitTypeId.DRONE): self.build_step += 1
        
        if self.build_step == 5:
            if self.minerals >= 190:
                utags = self.unit_tracker.rename('drone_natural', prev_name='', amount=1, unit_type_id=UnitTypeId.DRONE)
                if utags:
                    u = self.all_units.find_by_tag(utags[0])
                    u.smart(self.info_tracker.query('base_1_location'))
                    self.build_step += 1
        
        if self.build_step == 6:
            if self.can_afford(UnitTypeId.HATCHERY):
                utags = self.unit_tracker.select('drone_natural', amount=1, unit_type_id=UnitTypeId.DRONE)
                if utags:
                    u = self.all_units.find_by_tag(utags[0])
                    self.unit_tracker.queue(UnitTypeId.HATCHERY, 'base_1')
                    u.build(UnitTypeId.HATCHERY, self.info_tracker.query('base_1_location'))
                    self.build_step += 1
        
        if self.build_step == 7:
            if self.random_larva_train_and_track(UnitTypeId.DRONE): self.build_step += 1
            
        if self.build_step == 8:
            if self.random_larva_train_and_track(UnitTypeId.DRONE, name='drone_first_gas'): self.build_step += 1
        
        if self.build_step == 9:
            if self.random_larva_train_and_track(UnitTypeId.DRONE, name='drone_pool'): self.build_step += 1
        
        if self.build_step == 10:
            utags = self.unit_tracker.select('drone_first_gas', amount=1, unit_type_id=UnitTypeId.DRONE)
            if utags:
                u = self.all_units.find_by_tag(utags[0])
                min_distance = 99999
                for vg in self.vespene_geyser:
                    distance = vg.distance_to(u)
                    if distance < min_distance:
                        min_distance = distance
                        self.info_tracker.store('gas_first', vg)
            
            if self.info_tracker.query('gas_first'):
                self.build_step += 1
        
        if self.build_step == 11:
            utags = self.unit_tracker.select('drone_first_gas', amount=1, unit_type_id=UnitTypeId.DRONE)
            if utags:
                u = self.all_units.find_by_tag(utags[0])
                if self.can_afford(UnitTypeId.EXTRACTOR):
                    self.unit_tracker.queue(UnitTypeId.EXTRACTOR, 'gas_first')
                    u.build_gas(self.info_tracker.query('gas_first'))
                    self.build_step += 1
        
        if self.build_step == 12:
            map_center = self.game_info.map_center
            l_pool = self.start_location.towards(map_center, distance=5)
            self.info_tracker.store('pool_location', l_pool)
            self.build_step += 1
        
        if self.build_step == 13:
            utags = self.unit_tracker.select('drone_pool', amount=1, unit_type_id=UnitTypeId.DRONE)
            if utags:
                u = self.all_units.find_by_tag(utags[0])
                u.smart(self.info_tracker.query('pool_location'))
                self.build_step += 1
        
        if self.build_step == 14:
            if self.can_afford(UnitTypeId.SPAWNINGPOOL):
                utags = self.unit_tracker.select('drone_pool', amount=1, unit_type_id=UnitTypeId.DRONE)
                if utags:
                    u = self.all_units.find_by_tag(utags[0])
                    u.build(UnitTypeId.SPAWNINGPOOL, self.info_tracker.query('pool_location'))
                    self.build_step += 1
        
        if self.build_step == 15:
            if self.random_larva_train_and_track(UnitTypeId.DRONE, name='drone_mine_first_gas'): self.build_step += 1
        
        if self.build_step == 16:
            if self.random_larva_train_and_track(UnitTypeId.DRONE, name='drone_mine_first_gas'): self.build_step += 1
            
        if self.build_step == 17:
            if self.random_larva_train_and_track(UnitTypeId.DRONE): self.build_step += 1
        
        if self.build_step == 18:
            utags = self.unit_tracker.select('', amount=1, unit_type_id=UnitTypeId.DRONE)
            gas_tags = self.unit_tracker.select('gas_first', amount=1, unit_type_id=UnitTypeId.EXTRACTOR)
            if utags and gas_tags:
                g = self.all_units.find_by_tag(gas_tags[0])
                u = self.all_units.find_by_tag(utags[0])
                u.smart(g)
                if self.unit_tracker.rename_tag(utags[0], 'drone_mine_first_gas_ok'):
                    self.build_step += 1
        
        if self.build_step == 19:
            utags = self.unit_tracker.select('drone_mine_first_gas', amount=1, unit_type_id=UnitTypeId.DRONE)
            gas_tags = self.unit_tracker.select('gas_first', amount=1, unit_type_id=UnitTypeId.EXTRACTOR)
            
            if utags and gas_tags:
                g = self.all_units.find_by_tag(gas_tags[0])
                u = self.all_units.find_by_tag(utags[0])
                u.smart(g)
                if self.unit_tracker.rename_tag(utags[0], 'drone_mine_first_gas_ok'):
                    self.build_step += 1
                
        if self.build_step == 20:
            utags = self.unit_tracker.select('drone_mine_first_gas', amount=1, unit_type_id=UnitTypeId.DRONE)
            gas_tags = self.unit_tracker.select('gas_first', amount=1, unit_type_id=UnitTypeId.EXTRACTOR)
            
            if utags and gas_tags:
                g = self.all_units.find_by_tag(gas_tags[0])
                u = self.all_units.find_by_tag(utags[0])
                u.smart(g)
                if self.unit_tracker.rename_tag(utags[0], 'drone_mine_first_gas_ok'):
                    self.build_step += 1
        
        if self.build_step == 21:
            if self.random_larva_train_and_track(UnitTypeId.OVERLORD): self.build_step += 1
            
        if self.build_step == 22:
            if self.random_larva_train_and_track(UnitTypeId.DRONE): self.build_step += 1
            
        print(f'[INFO] {iteration} : reached build_step={self.build_step}')
        
        if self.build_step == 23:
            if len(self.townhalls) == 2 and self.structures(UnitTypeId.SPAWNINGPOOL).ready and self.minerals >= 300:
                for t in self.townhalls:
                    t.build(UnitTypeId.QUEEN)
                self.build_step += 1
        
        if self.build_step == 24:
            if self.random_larva_train_and_track(UnitTypeId.ZERGLING): self.build_step += 1
        
        if self.build_step == 25:
            if self.random_larva_train_and_track(UnitTypeId.ZERGLING): self.build_step += 1
        
        if self.build_step == 26:
            if self.vespene >= 100:
                
                
        # if self.build_step == 21:
        #     if self.can_afford(UnitTypeId.ZERGLING) and self.larva:
        #         selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
        #         if selected_larva:
        #             selected_larva.random(AbilityId.LARVATRAIN_ZERGLING, subtract_cost=True, subtract_supply=True)
        #             self.build_step = 22
                
        # if self.build_step == 22:
        #     if self.can_afford(UnitTypeId.ZERGLING) and self.larva:
        #         selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
        #         if selected_larva:
        #             selected_larva.random(AbilityId.LARVATRAIN_ZERGLING, subtract_cost=True, subtract_supply=True)
        #             self.build_step = 23
        
        # if self.build_step == 23:
        #     if self.can_afford(UnitTypeId.DRONE) and self.larva:
        #         selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
        #         if selected_larva:
        #             selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
        #             self.build_step = 24
        
        # if self.build_step == 24:
        #     if self.can_afford(UnitTypeId.DRONE) and self.larva:
        #         selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
        #         if selected_larva:
        #             selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
        #             self.build_step = 25
        
        # if self.build_step == 25:
        #     if self.can_afford(UnitTypeId.DRONE) and self.larva:
        #         selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
        #         if selected_larva:
        #             selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
        #             self.build_step = 26
        
        # if self.build_step == 26:
        #     if self.can_afford(UnitTypeId.DRONE) and self.larva:
        #         selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
        #         if selected_larva:
        #             selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
        #             self.build_step = 27
        
        # if self.build_step == 27:
        #     if self.can_afford(UnitTypeId.DRONE) and self.larva:
        #         selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
        #         if selected_larva:
        #             selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
        #             self.build_step = 28
        
        # if self.build_step == 28:
        #     if self.can_afford(UnitTypeId.DRONE) and self.larva:
        #         selected_larva = self.larva.filter(lambda u: u.tag not in self.unit_tags_received_action)
        #         if selected_larva:
        #             selected_larva.random(AbilityId.LARVATRAIN_DRONE, subtract_cost=True, subtract_supply=True)
        #             self.build_step = 29