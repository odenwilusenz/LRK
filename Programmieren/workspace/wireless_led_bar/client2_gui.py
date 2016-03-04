#client gui zum händischen wechseln der farben

import tkinter as tk
import time

import led_logic
import tcp_Comunication

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        x_size=26
        y_size=5
        
        self.active_painting_color=[0,0,0]
        self.sending=False
        
        
        self.createWidgets(x_size,y_size)#odysee2016 beschaltung
        #--die verschiedenen muster initialisieren--
        self.grid1=led_logic.Grid(x_size,y_size)
        self.rainbow=led_logic.Rainbow(self.grid1)
        self.rainbow.horizontal_wave_initial()
        
        
        #--netzwerk initialisieren
        self.sock=tcp_Comunication.TCP_Socket(None)
        self.protocol=tcp_Comunication.Protocol(None)
        
        self.do_ticks()

    def createWidgets(self,x_size,y_size):
        self.button_grid=[]
        for x in range(x_size):
            self.button_grid.append([])
            for y in range(y_size):
                but=self.add_button(x,y)
                self.button_grid[x].append([])
                self.button_grid[x][y]=but
                #print(self.button_grid[x][y])
        
        self.button1 = tk.Button(self, text="",command=self.do_button1)
        self.button1.grid(row=0, column=x_size+1)
        self.button2 = tk.Button(self, text="",command=self.do_button2)
        self.button2.grid(row=1, column=x_size+1)
        self.button3 = tk.Button(self, text="",command=self.do_button3)
        self.button3.grid(row=2, column=x_size+1)
        self.button4 = tk.Button(self, text="",command=self.do_button4)
        self.button4.grid(row=3, column=x_size+1)
        self.button5 = tk.Button(self, text="",command=self.do_button5)
        self.button5.grid(row=4, column=x_size+1)
        
        self.colorfield1=tk.Entry(self, bd =2,width=10)
        self.colorfield1.insert(0,"1,0,0")
        self.colorfield1.grid(row=0, column=x_size+2)
        self.colorfield2=tk.Entry(self, bd =2,width=10)
        self.colorfield2.insert(0,"0,1,0")
        self.colorfield2.grid(row=1, column=x_size+2)
        self.colorfield3=tk.Entry(self, bd =2,width=10)
        self.colorfield3.insert(0,"0,0,1")
        self.colorfield3.grid(row=2, column=x_size+2)
        self.colorfield4=tk.Entry(self, bd =2,width=10)
        self.colorfield4.insert(0,"0.5,0.5,0.5")
        self.colorfield4.grid(row=3, column=x_size+2)
        self.colorfield5=tk.Entry(self, bd =2,width=10)
        self.colorfield5.insert(0,"0,0,0")
        self.colorfield5.grid(row=4, column=x_size+2)
        
        self.do_button5()
        self.do_button4()
        self.do_button3()
        self.do_button2()
        self.do_button1()
        
        self.button_send = tk.Button(self, text="Start sending", fg="red",command=self.do_button_send)
        self.button_send.grid(row=y_size+1, column=x_size+1)

        self.QUIT = tk.Button(self, text="QUIT", fg="red",command=root.destroy)
        self.QUIT.grid(row=y_size+2, column=x_size+1)
    
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
    
    def _string_to_rgb(self,string):
        sub_str=string.split(",")
        res=[]
        for st in sub_str:
            res.append(float(st))
        return res[:3]
    
    def add_button(self,x,y,color='#00F000'):
        butt = tk.Button(self,bg=color, command=lambda row=x, column=y: self.button_click(row, column))
        butt.grid(row=y, column=x)
        return butt
    
    def button_click(self,x,y):
        #print("button_click",x,y)
        self.grid1.grid[x][y].set_color(self.active_painting_color)
        
    def do_button1(self):
        x=self.colorfield1.get()
        color=self._string_to_rgb(x)
        self.active_painting_color=color
        hex_string=self._rgb_to_hex(color)
        self.button1["bg"]=hex_string
        
    def do_button2(self):
        x=self.colorfield2.get()
        color=self._string_to_rgb(x)
        self.active_painting_color=color
        hex_string=self._rgb_to_hex(color)
        self.button2["bg"]=hex_string

    def do_button3(self):
        x=self.colorfield3.get()
        color=self._string_to_rgb(x)
        self.active_painting_color=color
        hex_string=self._rgb_to_hex(color)
        self.button3["bg"]=hex_string
        
    def do_button4(self):
        x=self.colorfield4.get()
        color=self._string_to_rgb(x)
        self.active_painting_color=color
        hex_string=self._rgb_to_hex(color)
        self.button4["bg"]=hex_string

    def do_button5(self):
        x=self.colorfield5.get()
        color=self._string_to_rgb(x)
        self.active_painting_color=color
        hex_string=self._rgb_to_hex(color)
        self.button5["bg"]=hex_string
      
    def do_button_send(self):
        if self.sending==True:
            self.sending=False
            self.button_send["text"]="Start sending"
        else:
            self.sending=True
            self.button_send["text"]="Stop sending"
            
    def do_ticks(self):
        new_grid=self.grid1#.get_led_matrix()
        self.update_button_colors(new_grid)
        if self.sending==True:
            msg=self.protocol.encode(new_grid)
            sock=tcp_Comunication.TCP_Socket(None)
            res=sock.send_message(msg,21001)
           #print("answer form send_message:",res)
            
        root.after(500, self.do_ticks)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()