# -*- coding: utf-8 -*-
"""
Created on Thu May  2 12:49:21 2013

@author: belza
"""
import threading
import sys
sys.path +=['..']
import libevents.events as events


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
        
        self.frame_queue = frame_queue
        self.ctrl_queue = ctrl_queue
        self.data_queue = data_queue
        self.mgmt_queue = mgmt_queue
        
        
    def run(self):
        frame = self.frame_queue.get()
        event = events.EventFrame(frmpkt =frame)
        if event.fr_type is "Mgmt":
            self.ctrl_queue.put(event,False)
        if event.fr_type is "Data":
            self.data_queue.put(event,False)
        if event.fr_type is "Ctrl":
            self.mgmt_queue.put(event,False)
        
        
        
def test():
   pass
    

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
        