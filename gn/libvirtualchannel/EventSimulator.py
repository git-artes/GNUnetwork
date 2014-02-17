#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Tue May  7 11:05:17 2013

@author: belza
'''

import sys
sys.path +=['..']
import libtimer.timer as Timer
import libevents.if_events as if_events
import threading,Queue,time



class EventSimulator(threading.Thread) :
    '''
    
    '''

    def __init__(self,tout,nickname,tx_event_q,my_addr,dst_addr):
        '''  
        Constructor.
        
        '''

        threading.Thread.__init__(self)
        self.finished = False    
        self.nickname =nickname
        self.my_addr = my_addr
        self.dst_addr =dst_addr
        self.my_queue = Queue.Queue(10)
        self.tout = tout
        self.tx_event_q =tx_event_q
        self.activateSimulator()
       
        
    def run(self):
        while not self.finished :
            event = if_events.mkevent(self.nickname)
            event.ev_dc['src_addr'] = self.my_addr
            event.ev_dc['dst_addr'] = self.dst_addr
            self.tx_event_q.put(event,False)
            aux= self.my_queue.get()
            if aux.nickname == "TimerTimer":
                timer=Timer.Timer(self.my_queue, \
                    self.tout,1,"TimerTimer")
                timer.start()

    def activateSimulator(self):
        timer=Timer.Timer(self.my_queue, \
            self.tout,1,"TimerTimer")
        timer.start()
    
    def stop(self):
        self.finished = True
        self._Thread__stop()



def test():
    myQueue=Queue.Queue(10)
    mySimulator = EventSimulator(5,"DataData",myQueue,100,101)
    mySimulator.start()
    while 1:
        event= myQueue.get()
        print " LLEGO EVENTO ", event, " ", int(round(time.time() * 1000)) 
   
    

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass


