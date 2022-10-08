# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 10:02:57 2022

@author: nghia_sv
"""

class InfoTracker:
    def __init__(self, info_keys):
        self.info = {}
        self.info_keys = []
        for key in info_keys:
            self.info[key] = None
    
    def query(self, key):
        if key in self.info:
            return self.info[key]
        else:
            return None
    
    def store(self, key, info):
        # assert key in self.info
        self.info[key] = info
