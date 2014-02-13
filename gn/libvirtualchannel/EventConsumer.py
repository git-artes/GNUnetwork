#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 12/02/2014

@author: ggomez
'''

import sys
sys.path +=['..']
import libevents.if_events as if_events
import threading,Queue,time

class EventConsumer(threading.Thread) :
    '''
    
    '''

    def __init__(self,nickname,rx_event_q):
        '''  
        Constructor.
        
        '''

        threading.Thread.__init__(self)
        self.finished = False    
        self.nickname = nickname
        self.rx_event_q = rx_event_q
        
    def run(self):
		while not self.finished :
			event = self.rx_event_q.get()
			print "Consumer ", self.nickname, "receive event: ", event

    def stop(self):
        self.finished = True
        self._Thread__stop()

def test():
   	rxQueue=Queue.Queue(10)

   	myConsumer = EventConsumer("L3consumer",rxQueue)
   	myConsumer.start()

	event = if_events.mkevent("CtrlRTS")
	event.ev_dc['src_addr'] = 100;
	event.ev_dc['dst_addr'] = 200;
	rxQueue.put(event,False)

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass


