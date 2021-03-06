from multiprocessing import Process, Queue, Lock
from receive import receive
from send import send
from heartbeat import heartbeat


def r_loop():
    
    rQueue = Queue()
    
    rLock = Lock()
    

    
    heartbeatPs = Process(target = heartbeat, args = ('localhost', 21567, 15))
    
    receivePs = Process(target = receive, args = (rQueue, rLock, 'localhost',
                                                   
    21567, 45))
    
    sendPs = Process(target =send, args = (rQueue, rLock))
    

    
    heartbeatPs.start()
    
    receivePs.start()
    

    sendPs.start()
    

    

    heartbeatPs.join()
    
    receivePs.join()
    

    sendPs.join()
    

if __name__ == '__main__':
    
    r_loop()

    

