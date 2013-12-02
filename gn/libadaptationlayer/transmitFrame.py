# -*- coding: utf-8 -*-
"""
Created on Thu May  2 12:49:21 2013

@author: belza
"""
import threading,Queue
import sys

sys.path +=['..']
import libevents.evstrframes as evstrframes
# The next import is defined only for test
import libevents.if_events as if_events



class TransmitFrame(threading.Thread):
    '''Puts L1 frames into a queue, gets events from the L2 queues AND generates frames.
    '''
    
    def __init__(self, frame_queue, event_queue):
        '''  
        Constructor
        
        @param frame_queue : The queue to put the L1 frames.
        @param event_queue : The queue to get L2 events .
        '''
        threading.Thread.__init__(self)
        self.frame_queue = frame_queue
        self.event_queue = event_queue
        self.finished=False
        
    def run(self):
        while not self.finished:
            event = self.event_queue.get()
            frame= evstrframes.mkframe(event)
            self.frame_queue.put(frame,False)
        
        
    def stop(self):
            self.finished = True
            self._Thread__stop()


        
def test():
    ev = if_events.mkevent("MgmtBeacon", ev_dc={'src_addr':'100','dst_addr':'150'})
    frame_q = Queue.Queue(10)
    ev_q = Queue.Queue(10)
    tr = TransmitFrame(frame_q,ev_q)
    tr.start()
    ev_q.put(ev,False)
        
    frame = frame_q.get()

    print "Frame = ", frame     
    

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass


