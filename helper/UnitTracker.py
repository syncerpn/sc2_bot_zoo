# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 21:28:30 2022

@author: nghia_sv
"""

from sc2.ids.unit_typeid import UnitTypeId

class UnitTracker:
    def __init__(self):
        self.units = {}
        self.name_queue = {}
        
        for utid in UnitTypeId:
            self.units[utid] = {}
            self.name_queue[utid] = []
    
    def __repr__(self):
        repr_str = ''
        for utid in UnitTypeId:
            if utid not in self.units:
                continue
            
            if not self.units[utid]:
                continue
            
            repr_str += f'{str(utid)}:\n'
            for utag in self.units[utid]:
                repr_str += f'\t{utag} : {self.units[utid][utag]}\n'
        
        return repr_str
    
    def queue(self, unit_type_id, name):
        self.name_queue[unit_type_id].append(name)
    
    def update(self, units_reference_list):
        #tracking every step: add tag to tracker and remove unavailable tags
        for u in units_reference_list:
            if not u.is_mine:
                continue
            
            utid = u.type_id
            utag = u.tag
            
            if utag == 0: #special (unknown why??) case with EXTRACTOR; it first morph with tag = 0, then the tag change; type id does not change though
                continue
            
            if utag not in self.units[utid]:
                if self.name_queue[utid]:
                    print(f'[INFO] UnitTracker: assigned name "{self.name_queue[utid][0]}" to a unit of type {utid.name} (tag={utag})')
                    self.units[utid][utag] = self.name_queue[utid][0]
                    self.name_queue[utid] = self.name_queue[utid][1:]
                else:
                    self.units[utid][utag] = ''
            
        to_be_removed = {}
        for utid in self.units:
            for utag in self.units[utid]:
                if not units_reference_list.find_by_tag(utag):
                    if utid not in to_be_removed:
                        to_be_removed[utid] = []
                        
                    to_be_removed[utid].append(utag)
        
        for utid in to_be_removed:
            for utag in to_be_removed[utid]:
                del self.units[utid][utag]
        #tracking end
    
    def select(self, name, amount=0, unit_type_id=None):
        selected = []
        for utid in self.units:
            if unit_type_id:
                if utid != unit_type_id:
                    continue
                
            for utag in self.units[utid]:
                if self.units[utid][utag] == name:
                    selected.append(utag)
                    if amount > 0:
                        if len(selected) >= amount:
                            break
                    
        print(f'[INFO] UnitTracker: select {amount if amount > 0 else "all"} "{name}" of type {unit_type_id.name if unit_type_id else "any"} ({len(selected)} selected)')
        return selected
    
    def rename_tag(self, utag, name):
        for utid in self.units:
            if utag in self.units[utid]:
                self.units[utid][utag] = name
                return True
        
        return False
    
    def rename(self, name, prev_name='', amount=0, unit_type_id=None):
        selected = []
        for utid in self.units:
            if unit_type_id:
                if utid != unit_type_id:
                    continue
                
            for utag in self.units[utid]:
                if self.units[utid][utag] == prev_name:
                    selected.append(utag)
                    self.units[utid][utag] = name
                    if amount > 0:
                        if len(selected) >= amount:
                            break
                    
        print(f'[INFO] UnitTracker: rename {amount if amount > 0 else "all"} of type {unit_type_id.name if unit_type_id else "any"} from "{prev_name}" to "{name}" ({len(selected)} renamed)')
        return selected