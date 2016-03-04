#snake game for lrk

import sys

import numpy as np
import matplotlib.pyplot as plt
import random

import led_logic


class Snake():
    def __init__(self,grid):
        self.grid=grid
        self.tick_nr=0
    
    def start(self):
        head_positio=[5,5]
        initial_tick=0
        tab=self.grid.get_led_matrix()
        for x in range(len(tab)):
            for y in range(len(tab[x])):
                tab[x][y].set_tick_nr(0)
            
    def tick(self):
        tab=self.grid.get_led_matrix()
        for x in range(len(tab)):
            for y in range(len(tab[x])):
                tick=tab[x][y].get_tick_nr()
                self.led_tick(tab[x][y],tick)
                tab[x][y].set_tick_nr(tick+1)
        self.tick_nr+=1
        return self.grid
    
    def led_tick(self,led,tick):#rainboweffect for a single led
        if led.get_color()==[0,0,0]:
            rnd=random.randint(0,50)
            if rnd==0:
                led.set_color((1,1,1))
        else:
            led.shift_color([-0.2,-0.2,-0.2])

if __name__ == "__main__":
    print("not ruable in standalone, use gui-application")
    