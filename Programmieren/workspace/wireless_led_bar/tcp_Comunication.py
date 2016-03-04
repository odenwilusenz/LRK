#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tcp-komunikation

Created on 04.08.2015

@author: Patrik-Schlatter
"""

import queue
import sys
import socket
import threading
import time
import traceback

import led_logic

#klasse zum en/decodieren des selbstdefinierten protkolls
class Protocol():
    def __init__(self,parent,*args,**kwargs):
        self.x_size=26
        self.y_size=5
        self.new_grid=led_logic.Grid(self.x_size,self.y_size)
    
    def encode(self,led_grid):
        #print("led_grid",led_grid)
        #print("plot",led_grid.plot())
        grid=led_grid.get_led_matrix()
        encoded_frame=""
        for y in range(len(grid[:][0])):
            for x in range(len(grid)):
                #print(self.grid[x][y].get_color())
                temp=grid[x][y].get_color()
                temp_str=""
                for element in temp:
                    temp_str+=str(element)+","#farben trenner code
                temp_str+=";" #led trenner code
                encoded_frame+=temp_str
                #encoded_frame+=temp.replace(" ","")
            encoded_frame=encoded_frame[:-1]#letztes trennzeichen entfernen
            encoded_frame+="#"#next Line code
        encoded_frame=encoded_frame[:-1]#letztes trennzeichen entfernen
        #print("total encoded frame",encoded_frame)
        return encoded_frame
    
    def decode(self,tcp_block):
        #print("trying to decode block",tcp_block)
        matrix=self.new_grid.get_led_matrix()
        linesplit=tcp_block.split("#")
        #print("linesplit",linesplit)
        
        y=0
        for line in linesplit:
            led_split=line.split(";")
            #print("led_split",led_split)
            x=0
            for led in led_split:
                color_split=led.split(",")
                #print ("led",led)
                #print("xy",x,y)
                matrix[x][y].set_color([float(color_split[0]),float(color_split[1]),float(color_split[2])])
                x+=1
                
            y+=1
        #TODO: validity checking for frame
        #print(matrix)
        return matrix


#Interprozesskomunikation via TCP-Sockets
##TODO: meherere Sockets gleichzeitig empfangen können (zum teil bereits strukturen dafür angelegt)
class TCP_Socket():
    def __init__(self,parent,*args,**kwargs):
        self.thread_list=[]
        self.socket_list=[]
        #ip_address='localhost'
        self.ip_address="10.248.4.150"
        
    #sendet die Nachricht an den angegebenen lokalen Port.
    def send_message(self,message,port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# create an INET, STREAMing socket
            s.connect((self.ip_address, port))
            message+="#end#"
            s.sendall(message.encode())#end-marker für nachricht anhängen
            return True
        except:
            print(traceback.format_exc())
            return False
        finally:
            s.close()#socket wieder schliessen

    
    #macht falls nötig einen Scket auf und gibt die queue zum angegebenen Socket zurück. 
    def get_serversocket_queue(self,port):
        #--checken ob schone ein socket für diesen port offen ist
        #print "self.socket_list",self.socket_list
        for entry in self.socket_list:
            if entry[0]==port:
                return entry[1]
        #--neuen socket anlegen
        my_queue=self._open_serversocket(port)
        self.socket_list.append([port,my_queue])
        return my_queue

    #Öffnet einene Serversocket und startet den SocketListenerThread. gibt die Queue zurück, auf der die Messenges liegen
    def _open_serversocket(self,port,max_connections=1):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create an INET, STREAMing socket
        #serversocket.bind(('localhost', port)) # bind the socket to a public host, and a well-known port
        #serversocket.bind((socket.gethostname(), port)) # bind the socket to a public host, and a well-known port
        serversocket.bind(("", port)) # bind the socket to a public host, and a well-known port 
        
        serversocket.listen(max_connections)
        
        my_queue=queue.Queue()
        thread=SocketListenerThread(serversocket,my_queue)
        thread.setDaemon(True)
        self.thread_list.append(thread)
        thread.start()
        return my_queue

#     def close_all_serversockets(self):
#         print "stopping all socket-threads"
#         for thread in self.thread_list:
#             thread.stop()
#         #for thread in self.thread_list:
#         #    thread.join()
#         self.thread_list=[] #TODO: sicherstellen das während dem schliessen keine neuen sockets aufgemacht werden
#         print "all sockets closed"
            
class SocketListenerThread(threading.Thread): #einfache messung
    def __init__(self,socket_list,my_queue,*args,**kwargs):
        super(SocketListenerThread,self).__init__()
        self.socket_list=socket_list
        self.my_queue=my_queue
        self.stop_requested=False

    def run(self):
        try:
            #print("SocketListenerThread started")
            while True:
                #for single_socket in self.socket_list:
                (clientsocket, address) = self.socket_list.accept()
                #print "socket_thread: ",clientsocket,address
                #Daten empfangen
                msg_buffer=""
                while True:
                    data = clientsocket.recv(16).decode()
                    if data!="":
                        msg_buffer+=data
                        if msg_buffer.find("#end#")>0:
                            #print "found end"
                            end=msg_buffer.find("#end#")
                            message=msg_buffer[:end]
                            #print("got message", message)
                            self.my_queue.put(message)
                            break
                    if self.stop_requested==True:
                        #print("socket-thread stopping...")
                        return
                        #TODO: ev hier keinen stop_requested austieg, da übertagung abgebrochen wird?
                if self.stop_requested==True:
                    #print("socket-thread stopped")
                    return
                #print "thread alive"
                #time.sleep(0.1)
        except:
            print(traceback.format_exc())
    
    def stop(self):
        #print("stop thread")
        self.stop_requested=True

if __name__ == '__main__':     
    sock=TCP_Socket(None)
    my_queue=sock.get_serversocket_queue(port=21001)
    print("test")
    time.sleep(2)
    res=sock.send_message("hallo welt#end#",21001)
    print("sent",res)
    time.sleep(2)
    res=sock.send_message("hello again#end#",21001)
    print("sent",res)
    time.sleep(2)
    try:
        for _ in range(5):
            print(my_queue.get_nowait())
    except queue.Empty:
        print("queue empty")
