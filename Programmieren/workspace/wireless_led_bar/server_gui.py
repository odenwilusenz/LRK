import sys
import queue
import tkinter as tk
import time
import threading
import traceback

import led_logic
import common_gui_components as gui_commons
import tcp_Comunication

import lrkmaster

class Application(tk.Frame,gui_commons.UI):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        gui_commons.UI.__init__(self)
        self.grid()
        x_size=24
        y_size=5
        self.nr_of_streams=5
        self.createWidgets(x_size,y_size)
        self.grid1=led_logic.Grid(x_size,y_size)
        self.protocol=tcp_Comunication.Protocol(self)
        
        sock=tcp_Comunication.TCP_Socket(None)
        
        self.my_queue=sock.get_serversocket_queue(port=21000)
        
        self.led_queue=queue.Queue()
        thread=PushOverToLedTread(self.led_queue)
        thread.setDaemon(True)
        thread.start()
        
        #self.lrk=lrkmaster.LRKmaster("/dev/ttyUSB0")
        
#         print("test")
#         time.sleep(2)
#         msg="1,1,1,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,#0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,#0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,#0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,#0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0,0,0.01,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0.01,0,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,;0,0.01,0,"
#         res=sock.send_message(msg,21000)
#         print("sent",res)
#         time.sleep(2)


#         self.rainbow=led_logic.Rainbow(self.grid1)
#         self.rainbow.horizontal_wave_initial()
        self.update_preview()

    def createWidgets(self,x_size,y_size):
        self.button_grid=[]
        for x in range(x_size):
            self.button_grid.append([])
            for y in range(y_size):
                but=self.add_button(x,y)
                self.button_grid[x].append([])
                self.button_grid[x][y]=but
                #print(self.button_grid[x][y])
                
        for nr in range(self.nr_of_streams):
            self.label = tk.Label(self,text="Stream "+str(nr))
            self.label.grid(row=nr, column=x_size+1)
            self.test1 = tk.Button(self, text="Preview", fg="red",command=self.do_test1)
            self.test1.grid(row=nr, column=x_size+2)
            self.test1 = tk.Button(self, text="Output", fg="red",command=self.do_test1)
            self.test1.grid(row=nr, column=x_size+3)
        
        self.QUIT = tk.Button(self, text="QUIT", fg="red",command=root.destroy)
        self.QUIT.grid(row=9, column=x_size+1)

    def update_preview(self):
        try:
            frame=self.my_queue.get_nowait()
            #print("got message via queue",frame)
            new_grid=self.protocol.decode(frame)
            self.update_button_colors(new_grid)
            
            self.led_queue.put(new_grid)
            
            
#             with lrkmaster.LRKmaster("/dev/ttyUSB0") as lrk:
#                 x_list = [1,3,5,7,9,11,15,17,19,21,23]
#                 for y in range(1,6):
#                     for x in x_list:
#                         try:
#                             led1=new_grid[x-1][y-1].get_color()
#                             led2=new_grid[x][y-1].get_color()
#                             print("leds",x,y,led1,led2)
#                             lrk.do(y, x, int(led1[0]*255), int(led1[1]*255), int(led1[2]*255), int(led2[0]*255), int(led2[1]*255), int(led2[2]*255))
#                         except lrkmaster.LRKError:
#                             print(("led module",x,y,"not responding"))
                        
                #self.lrk.do(row, place, r1, g1, b1, r2, g2, b2)            

        except queue.Empty:
            pass
            #print("queue empty")

        root.after(10, self.update_preview)#update nach x wieder aufrufen

#     def update_button_colors(self,grid):
#         tab=grid.get_led_matrix()
#         for x in range(len(tab)):
#             for y in range(len(tab[0])):
#                 rgb=tab[x][y].get_color()
#                 hex_string=self._rgb_to_hex(rgb)
#                 #print("rgb:",rgb,"hex",hex_string)
#                 self.button_grid[x][y]["bg"]=hex_string#'#000000'
#                 
#     def _rgb_to_hex(self,rgb):
#         hex_r=self._hex_string(int(rgb[0]*255))
#         hex_g=self._hex_string(int(rgb[1]*255))
#         hex_b=self._hex_string(int(rgb[2]*255))
#         hex_str="#"+hex_r+hex_g+hex_b
#         #print("rgb",rgb,"hex_str",hex_str)
#         return hex_str
#     
#     def _hex_string(self,integer):
#         h=str(hex(integer)).replace("0x","")
#         if len(h)==1:
#             h="0"+h
#         return h
#     
#     def add_button(self,x,y,color='#00F000'):
#         hi_there = tk.Button(self,bg=color)
#         #self.hi_there["text"] = "x"
#         hi_there["command"] = self.say_hi
#         hi_there.grid(row=y, column=x)
#         return hi_there
#     
#     def say_hi(self):
#         print("hi there, everyone!")
#         
#     def do_test1(self):
#         new_grid=self.rainbow.tick()
#         self.update_button_colors(new_grid)
#         root.after(50, self.do_test1)
#         
#     def do_test2(self):
#         print("bar")
#         self.button_grid[5][2]["bg"]='#000000'


class PushOverToLedTread(threading.Thread): #einfache messung
    def __init__(self,input_queue,*args,**kwargs):
        super(PushOverToLedTread,self).__init__()
        self.input_queue=input_queue

    def run(self):
        try:
            
            with lrkmaster.LRKmaster("/dev/ttyUSB0") as lrk:
  
                while True:
                
                    #new_grid=self.input_queue.get_nowait()
                    new_grid=self.input_queue.get()
                
                    x_list = [1,3,5,7,9,11,15,17,19,21,23]
                    for y in range(1,6):
                        for x in x_list:
                            try:
                                led1=new_grid[x-1][y-1].get_color()
                                led2=new_grid[x][y-1].get_color()
                                #print("leds",x,y,led1,led2)
                                lrk.do(y, x, int(led1[0]*255), int(led1[1]*255), int(led1[2]*255), int(led2[0]*255), int(led2[1]*255), int(led2[2]*255))
                            except lrkmaster.LRKError:
                                print(("led module",x,y,"not responding"))

        except:
            print(traceback.format_exc())


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()