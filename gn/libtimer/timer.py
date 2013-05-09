# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 14:31:45 2012

@author: belza
"""
import threading, time,Queue
import sys
sys.path +=sys.path + ['..']
import libevents.events as events

class Timer(threading.Thread):
    """ This class is a timer (is a Thread) that waits for a given interval. After that generates an event of Type TIMER and SUPTYPE the name given in subTypeEvent1.
         The timer retries the number of times gven in the parameter retry. After the given number of retries generates the event of TYPE TIMER and subtype given in subTypeEvent2 if it is not None.    
    """
    def __init__(self, q_event, interval, retry,subTypeEvent1,add_info =None,subTypeEvent2=None ):
        '''  
        Constructor
        
        @param q_event : The event queue where the events must be inserted.

        @param interval : The interval of time.

        @param retry : The number of retries.
        
        @param subTypeEvent1 : The subtype of the event that must be called after each retry.
        
        @param subTypeEvent2 : The subtype of the event that must be called after the given number of retries.
        
        @param add_info : additional information that will be send with the Timer Event        
        
        '''        
        
        
        
        threading.Thread.__init__(self)
        self.interval = interval
        self.retry = retry
        self.subTypeEvent1=subTypeEvent1
        self.subTypeEvent2=subTypeEvent2
        self.add_info = add_info
        self.q_event = q_event
        
    def run(self):
        """ This is the private thread that generates ."""
        for i in range(self.retry):    
            time.sleep(self.interval)
            self.tout1()
        if self.subTypeEvent2 is not None:
            self.tout2()                
        
    def tout1(self):      
            event= events.EventTimer("Timer",self.subTypeEvent1,self.add_info)
            self.q_event.put(event,False)
    def tout2(self):
            event= events.EventTimer("Timer",self.subTypeEvent2,self.add_info)
            self.q_event.put(event,False)    
                

def test():
    myQueue=Queue.Queue(10)
    myTimer = Timer(myQueue,0.5,10,"TOR1",None,"TOR2")
    myTimer.start()
    aux=""
    while aux  is not "TOR2":
        event= myQueue.get()
        aux = event.ev_subtype
        print " LLEGO EVENTO ", event.ev_subtype, " ", int(round(time.time() * 1000)) 
   
    

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
