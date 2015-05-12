import socket
import multiprocessing
import time


def heartbeat(host, port, beat_period):
  
     ADDR = (host,port)
    
     sock =socket.socket(socket.AF_INET ,socket.SOCK_DGRAM)
    
     thStop = False
  
     while not thStop:
 
           sock.sendto('PyHB', ADDR)
          
           time.sleep(beat_period)
