import sys

import numpy as np
#import matplotlib.pyplot as plt
import random


class Led():
    """einzelnes LED, respektive LED-Band"""
    def __init__(self):
        self.color=[0,0,0]#anfangsfarbe
        self.tick=0
    
    def set_color(self,rgb):
        #--sanatize input--
        if rgb[0]>1:
            r=1
        elif rgb[0]<0:
            r=0
        else:
            r=rgb[0]
        if rgb[1]>1:
            g=1
        elif rgb[1]<0:
            g=0
        else:
            g=rgb[1]
        if rgb[2]>1:
            b=1
        elif rgb[2]<0:
            b=0
        else:
            b=rgb[2]
        #--set values--
        self.color=[r,g,b]
        #TODOrgb: farbänderung übermitteln
    
    def get_color(self):
        return self.color
    
    def get_tick_nr(self):
        return self.tick
        
    def set_tick_nr(self,tick_nr):
        self.tick=tick_nr
        return tick_nr
    
    def shift_color(self,rgb):
        self.color[0]+=rgb[0]
        self.color[1]+=rgb[1]
        self.color[2]+=rgb[2]
        self.set_color(self.color)#werte wieder begrenzen
    
class Grid():
    """Gitterstruktur aus LEDs"""
    def __init__(self,grid_lengh,grid_with):
        self.grid=self._generate_grid(grid_lengh,grid_with)
        
    def _generate_grid(self,grid_lengh,grid_with):
        new_grid=[]
        for l in range(grid_lengh):
            new_grid.append([])
            for w in range(grid_with):
                new_grid[l].append([])
                new_grid[l][w]=Led()
        return new_grid
        
    def plot(self):
        """rudimentäre plot funktion für das led-grid"""
        for y in range(len(self.grid[:][0])):
            for x in range(len(self.grid)):
                #print(self.grid[x][y].get_color())
                sys.stdout.write(str(self.grid[x][y].get_color()))
            sys.stdout.write("\n")
                
    def get_led_matrix(self):
        return self.grid
        
class Rainbow():
    def __init__(self,grid):
        self.grid=grid
        self.tick_nr=0
    
    def horizontal_wave_initial(self):
        initial_tick=0
        tab=self.grid.get_led_matrix()
        for x in range(len(tab)):
            for y in range(len(tab[x])):
                #tab[x][y].set_color((x/10.0,y/10.0,0))
                tab[x][y].set_tick_nr(initial_tick)
                initial_tick+=1
            initial_tick+=10
            
    def vertical_wave_initial(self):
        tab=self.grid.get_led_matrix()
        for x in range(len(tab)):
            initial_tick=0
            for y in range(len(tab[x])):
                #tab[x][y].set_color((x/10.0,y/10.0,0))
                tab[x][y].set_tick_nr(initial_tick)
                initial_tick+=15

            
    def diagonal_wave_initial(self):
        initial_tick=0
        tab=self.grid.get_led_matrix()
        for x in range(len(tab)):
            for y in range(len(tab[x])):
                #tab[x][y].set_color((x/10.0,y/10.0,0))
                tab[x][y].set_tick_nr(initial_tick)
                initial_tick+=1
            initial_tick+=-10
            
    def tick(self):
        #print("rainbow_tick")
        tab=self.grid.get_led_matrix()
        for x in range(len(tab)):
            for y in range(len(tab[x])):
                tick=tab[x][y].get_tick_nr()
                self.led_tick(tab[x][y],tick)
                tab[x][y].set_tick_nr(tick+1)
        self.tick_nr+=1
        return self.grid
    
    def led_tick(self,led,tick):#rainboweffect for a single led
        stepsize=0.01
        angle_point=1/stepsize
        tick=tick%(angle_point*3) #widerholt sich nach x animationsschritten
#         if tick==0:
#             led.set_color((1,0,0))#anfangsstatus
        if tick < angle_point:
            led.shift_color((-stepsize,+stepsize,0))
        elif tick < angle_point*2:
            led.shift_color((0,-stepsize,+stepsize))
        elif tick < angle_point*3:
            led.shift_color((+stepsize,0,-stepsize))
        #print(led.get_color(),self.tick_nr)
        
#     def wandering_rainnbow(self):
#         pass
#     
#     def disco(self):
#         pass
#     
#     def random(self):
#         random.random()
#     
#     def explosion(self,start_position=(0,0)):
#         pass
        

class Sparkle():
    def __init__(self,grid):
        self.grid=grid
        self.tick_nr=0
    
    def initial(self):
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

class Worm():
    def __init__(self,grid):
        self.grid=grid
        self.tick_nr=0
        self.momentan_color=[1,0,0]
    
    def initial(self):
        initial_tick=0
        tab=self.grid.get_led_matrix()
        for x in range(len(tab)):
            for y in range(len(tab[x])):
                tab[x][y].set_tick_nr(0)
            
    def tick(self):
        tab=self.grid.get_led_matrix()
        tick=tab[0][0].get_tick_nr()
        #--head--
        #print(((int(tick/26))%5)%2)
        new_color=[]
        for i in self.momentan_color:
            x=i+(random.random()-0.5)/4
            if x>1:
                x=1
            elif x<0:
                x=0
            new_color.append(x)
        if (int(tick/26)%5)%2==0:
            tab[(tick%26)][(int(tick/26))%5].set_color(new_color)
        else:
            tab[25-(tick%26)][(int(tick/26))%5].set_color(new_color)
        self.momentan_color=new_color
        #--tail--
        for x in range(len(tab)):
            for y in range(len(tab[x])):
                self.led_tick(tab[x][y],tick)
                tab[x][y].set_tick_nr(tick+1)
        self.tick_nr+=1
        return self.grid
    
    def led_tick(self,led,tick):#rainboweffect for a single led
        col=led.get_color()
        if (col[0]>0)or(col[1]>0)or(col[2]>0):
            led.shift_color([-0.01,-0.01,-0.01])      
        else:
            led.set_color((0,0,0))

        
if __name__ == "__main__":
    print("start")
    grid_lengh=20
    grid_with=5
    grid=Grid(grid_lengh,grid_with)
    print("ende")
    