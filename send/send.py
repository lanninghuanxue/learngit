import pika

import multiprocessing



def send(nQueue,nLock):
  
    connection = pika.BlockingConnection(pika.ConnectionParameters(
             host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='wrong')
    
    rQueue = nQueue
    
    rLock = nLock


    
    while True:
             
        item = rQueue.get()
  
        if item == 'wrong':
            

            channel.basic_publish(exchange='',
                      routing_key='wrong',
                      body='wrong!')
    



