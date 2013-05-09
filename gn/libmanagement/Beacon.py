# -*- coding: utf-8 -*-
"""
Created on Tue May  7 11:05:17 2013

@author: belza
"""

import sys
sys.path +=['..']
import libtimer.timer as Timer
import libevents.events as events
import threading,Queue,time
import NetworkConfiguration
class Beacon(threading.Thread) :
    """   The Beacon  is a Thread.
    
          This class control the Beacon generation.       
    """

    def __init__(self,network_conf,tx_event_q):
        '''  
        Constructor
        
        @param network_conf : actual network configuration.        
        @param tx_event_q : The event queue where the beacon events will be added.
        
        '''
        threading.Thread.__init__(self)
        self.my_addr = network_conf. getStationId()
        self.broadcast_addr =network_conf.getBroadcastAddr()
        self.my_queue = Queue.Queue(10)
        self.my_actual_net_conf = network_conf 
        self.tx_event_q =tx_event_q
        self.activateBeacon()
      
        
    def run(self):
        while 1:
            aux= self.my_queue.get()
            timer=Timer.Timer(self.my_queue, self.my_actual_net_conf.beacon_period,1,"Timer")
            timer.start()
            event = events.EventFrame("Mgmt","Beacon")
            self.tx_event_q.put(event,False)

    def activateBeacon(self):
        timer=Timer.Timer(self.my_queue, self.my_actual_net_conf.beacon_period,1,"Timer")
        timer.start()
        
        
        
def test():
    myQueue=Queue.Queue(10)
    net_conf1 = NetworkConfiguration.NetworkConfiguration(100,'my network',256,1)
    myBeacon = Beacon(net_conf1 ,myQueue)
    myBeacon.start()
    aux=""
    while 1:
        event= myQueue.get()
        aux = event.ev_subtype
        print " LLEGO EVENTO ", event.ev_subtype, " ", int(round(time.time() * 1000)) 
   
    

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
