# -*- coding: utf-8 -*-
"""
Created on Thu May  2 12:49:21 2013

@author: belza
"""
import threading,Queue
import sys
sys.path +=['..']
import libevents.if_events as events
" The next import is defined only for test"
import libevents.events as Events


class Scheduler(threading.Thread):
    """ This class gets L1 frames from a queue. It generates and puts events in the L2 queues (control, data, managenet).
    """
    
    def __init__(self,frame_queue,ctrl_queue, data_queue,mgmt_queue):
        '''  
        Constructor
        
          @param frame_queue : The queue to get the frames from the L1.

          @param ctrl_queue : The queue to put the control events.
          
          @param data_queue : The queue to put the data events.

          @param mgmt_queue : The queue to put the management events.


        '''
        threading.Thread.__init__(self)
        self.frame_queue = frame_queue
        self.ctrl_queue = ctrl_queue
        self.data_queue = data_queue
        self.mgmt_queue = mgmt_queue
        self.finished=False
        
    def run(self):
        while not self.finished:
            frame = self.frame_queue.get()
            event= events.mkevent(pframe=frame)
            if event.ev_type == "Ctrl":
                self.ctrl_queue.put(event,False)
            if event.ev_type == "Data":
                self.data_queue.put(event,False)
            if event.ev_type == "Mgmt":
                self.mgmt_queue.put(event,False)
        
        
    def stop(self):
            self.finished = True
            self._Thread__stop()


        
def test():
    ev = Events.mkevent("MgmtBeacon")
    ev.src_addr = "100"
    ev.dst_addr=  "150"
    frame_q = Queue.Queue(10)
    ctrl_q = Queue.Queue(10)
    mgmt_q = Queue.Queue(10)
    data_q = Queue.Queue(10)
    sch = Scheduler(frame_q,ctrl_q,data_q,mgmt_q)
    sch.start()
    
    frame=events.mkframe(ev)
    print " Frame = ", frame
    frame_q.put(frame,False)
    
    event = mgmt_q.get()

    print "Event = ", event
    

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
        
