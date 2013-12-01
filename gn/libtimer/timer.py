# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 14:31:45 2012

@author: belza
"""
import threading, time,Queue
import sys
sys.path +=sys.path + ['..']
import libevents.if_events as if_events

class Timer(threading.Thread):
    """ This class is a timer (is a Thread) that waits for a given interval. After that generates an event of Type TIMER and SUPTYPE the name given in subTypeEvent1.
         The timer retries the number of times gven in the parameter retry. After the given number of retries generates the event of TYPE TIMER and subtype given in subTypeEvent2 if it is not None.    
    """
    def __init__(self, q_event, interval, retry,nickname1,add_info =None,nickname2=None ):
        '''  
        Constructor
        
        @param q_event : The event queue where the events must be inserted.

        @param interval : The interval of time.

        @param retry : The number of retries.
        
        @param nickname1 : The nickname of the event that must be called after each retry.
        
        @param nickname2 : The nickname of the event that must be called after the given number of retries.
        
        @param add_info : additional information that will be send with the Timer Event        
        
        '''        
        
        
        
        threading.Thread.__init__(self)
        self.interval = interval
        self.retry = retry
        self.nickname1=nickname1
        self.nickname2=nickname2
        self.add_info = add_info
        self.q_event = q_event
        self.finished = False
        
    def run(self):
        """ This is the private thread that generates ."""
        for i in range(self.retry):    
            time.sleep(self.interval)
            if self.finished:
                return
            self.tout1()
        if self.nickname2 is not None:
            self.tout2()                
        
    def tout1(self):      
            event= if_events.mkevent(self.nickname1)
            event.add_info = self.add_info
            self.q_event.put(event,False)
    def tout2(self):
            event= if_events.mkevent(self.nickname2)
            event.add_info = self.add_info
            self.q_event.put(event,False)    
                
    def stop(self):
            self.finished = True
            self._Thread__stop()

def test():
    myQueue=Queue.Queue(10)
    myTimer = Timer(myQueue,0.5,10,"TimerTOR1",None,"TimerTOR2")
    myTimer.start()
    aux=""
    while aux  is not "TimerTOR2":
        event= myQueue.get()
        aux = event.nickname
        print " LLEGO EVENTO ", event, " ", int(round(time.time() * 1000)) 
   
    print "Segunda parte"
    myTimer = Timer(myQueue,0.5,10,"TimerTOR1",150,"TimerTOR2")
    myTimer.start()
    aux= 0
    while aux  < 3:
        event= myQueue.get()
        print " LLEGO EVENTO ", event, " add_info ", event.add_info, int(round(time.time() * 1000)) 
        aux += 1
    myTimer.stop()

    

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
