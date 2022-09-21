# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 21:28:30 2022

@author: nghia_sv
"""

class LarvaTracker:
    def __init__(self):
        self.consumed_larva_tag = []
        
    def get_and_consume_larva_random(self, larvas):
        selected_larva = None
        for larva in larvas:
            if larva.tag in self.consumed_larva_tag:
                continue
            else:
                selected_larva = larva
                self.consumed_larva_tag += [selected_larva.tag]
                break
        return selected_larva