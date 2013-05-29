# -*- coding: utf-8 -*-
"""
Created on Mon May 27 15:30:00 2013

@author: belza
"""

import sys
sys.path +=['..']

import threading, Queue,time


class VirtualChannel(threading.Thread) :
    
        
    """ This class simulates a communication channel.
        Every frame recieved in its queue is send it to the nodes queues        
    """
    def __init__(self, queue_rx):
        '''  
        Constructor: build an empty list and asign it reception queue    
        '''
        threading.Thread.__init__(self)
        self.node_list=[]
        self.queue_rx = queue_rx
        self.finished = False
    def add(self,node_queue):
        """
            
            @param node_queue:  the reception queue of a new node in the network.
        
        """
        self.node_list.append({'node_queue':node_queue})


    def run(self):
        while not self.finished:
            frame= self.queue_rx.get()
            for i in range(0,len(self.node_list)):
                self.node_list[i]['node_queue'].put(frame,False)
                
                
    def stop(self):
        self.finished=True
        self._Thread__stop()



def test():
    myQueue=Queue.Queue(10)
    vc= VirtualChannel(myQueue)
    rec_queue1= Queue.Queue(10) 
    rec_queue2= Queue.Queue(10)
    vc.add(rec_queue1)
    vc.add(rec_queue2)    
    vc.start()
    frame =100
    myQueue.put(frame,False)
    print "Queue 1 : ", rec_queue1.get()
    print "Queue 2 : ", rec_queue2.get()
    vc.stop()

   
    

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
        