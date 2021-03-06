#snake

import tkinter as tk
import time

import led_logic
import tcp_Comunication

import snake

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        x_size=24
        y_size=5
        
        self.createWidgets(x_size,y_size)#odysee2016 beschaltung
        #--die verschiedenen muster initialisieren--
        self.grid1=led_logic.Grid(x_size,y_size)
        
        self.snake=snake.Snake(self.grid1)
        self.snake.start()
#         self.rainbow=led_logic.Rainbow(self.grid1)
#         self.rainbow.horizontal_wave_initial()
        
        self.bind("<Left>", self.key_left)
        self.bind("<Right>", self.key_right)
        self.bind("<Up>", self.key_up)
        self.bind("<Down>", self.key_down)
        self.focus_set()
        
        #--netzwerk initialisieren
        self.sock=tcp_Comunication.TCP_Socket(None)
        self.protocol=tcp_Comunication.Protocol(None)
        
        self.active_pattern=None
        self.do_ticks()
        
    def key_left(self,event):
        print("left pressed")
    
    def key_right(self,event):
        print("right pressed")
        
    def key_up(self,event):
        print("up pressed")
        
    def key_down(self,event):
        print("down pressed")
    
    def createWidgets(self,x_size,y_size):
        self.button_grid=[]
        for x in range(x_size):
            self.button_grid.append([])
            for y in range(y_size):
                but=self.add_button(x,y)
                self.button_grid[x].append([])
                self.button_grid[x][y]=but
                #print(self.button_grid[x][y])
        
        self.button1 = tk.Button(self, text="Snake", fg="red",command=self.do_button1)
        self.button1.grid(row=0, column=x_size+1)
        self.button2 = tk.Button(self, text="", fg="red",command=self.do_button2)
        self.button2.grid(row=1, column=x_size+1)
        self.button3 = tk.Button(self, text="", fg="red",command=self.do_button3)
        self.button3.grid(row=2, column=x_size+1)
        self.button4 = tk.Button(self, text="", fg="red",command=self.do_button4)
        self.button4.grid(row=3, column=x_size+1)
        self.button5 = tk.Button(self, text="", fg="red",command=self.do_button5)
        self.button5.grid(row=4, column=x_size+1)

        self.QUIT = tk.Button(self, text="QUIT", fg="red",command=root.destroy)
        self.QUIT.grid(row=9, column=x_size+1)
    
    def update_button_colors(self,grid):
        tab=grid.get_led_matrix()
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
        
    def do_button1(self):
        self.active_pattern=1
        
    def do_button2(self):
        self.active_pattern=2

    def do_button3(self):
        self.active_pattern=3
        
    def do_button4(self):
        self.active_pattern=4
        
    def do_button5(self):
        self.active_pattern=5

    def do_ticks(self):
        if self.active_pattern==None:
            pass
        elif self.active_pattern==1:
            new_grid=self.snake.tick()
            self.update_button_colors(new_grid)
            msg=self.protocol.encode(new_grid)
            sock=tcp_Comunication.TCP_Socket(None)
            res=sock.send_message(msg,21000)
            #print("answer form send_message:",res)

        else:
            print("unknown active_pattern")
        root.after(200, self.do_ticks)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()