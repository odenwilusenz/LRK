import tkinter as tk
import time

import led_logic

# class Application(tk.Frame):
#     def __init__(self, master=None):
#         tk.Frame.__init__(self, master)
#         self.grid()
#         x_size=24
#         y_size=5
#         self.createWidgets(x_size,y_size)#odysee2016 beschaltung
#         self.grid1=led_logic.Grid(x_size,y_size)
#         self.rainbow=led_logic.Rainbow(self.grid1)
#         self.rainbow.horizontal_wave_initial()

class UI():
    def __init__(self):
        pass

    def createWidgets(self,x_size,y_size):
        self.button_grid=[]
        for x in range(x_size):
            self.button_grid.append([])
            for y in range(y_size):
                but=self.add_button(x,y)
                self.button_grid[x].append([])
                self.button_grid[x][y]=but
                #print(self.button_grid[x][y])
        
        self.test1 = tk.Button(self, text="Test1", fg="red",command=self.do_test1)
        self.test1.grid(row=0, column=x_size+1)
        self.test2 = tk.Button(self, text="Test2", fg="red",command=self.do_test2)
        self.test2.grid(row=1, column=x_size+1)
        
        self.QUIT = tk.Button(self, text="QUIT", fg="red",command=root.destroy)
        self.QUIT.grid(row=9, column=x_size+1)
    
    def update_button_colors(self,grid):
        tab=grid
        for x in range(len(tab)):
            for y in range(len(tab[0])):
                rgb=tab[x][y].get_color()
                hex_string=self._rgb_to_hex(rgb)
                #print("rgb:",rgb,"hex",hex_string)
                self.button_grid[x][y]["bg"]=hex_string#'#000000'
                
    def _rgb_to_hex(self,rgb):
        hex_r=self._hex_string(int(rgb[0]*255))
        hex_g=self._hex_string(int(rgb[1]*255))
        hex_b=self._hex_string(int(rgb[2]*255))
        hex_str="#"+hex_r+hex_g+hex_b
        #print("rgb",rgb,"hex_str",hex_str)
        return hex_str
    
    def _hex_string(self,integer):
        h=str(hex(integer)).replace("0x","")
        if len(h)==1:
            h="0"+h
        return h
    
    def add_button(self,x,y,color='#00F000'):
        hi_there = tk.Button(self,bg=color)
        #self.hi_there["text"] = "x"
        hi_there["command"] = self.say_hi
        hi_there.grid(row=y, column=x)
        return hi_there
    
    def say_hi(self):
        print("hi there, everyone!")
        
    def do_test1(self):
        new_grid=self.rainbow.tick()
        self.update_button_colors(new_grid)
        root.after(50, self.do_test1)
        
    def do_test2(self):
        print("bar")
        self.button_grid[5][2]["bg"]='#000000'

