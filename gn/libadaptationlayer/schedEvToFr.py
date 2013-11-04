#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sched-bytype.py
#


'''An scheduler that get an event  from Layer 2 input queue, generates the corresponding frame, and put it into the Layer 1 transmit queue .
'''
import Queue
import sys
sys.path +=['..']
import libevents.if_events as events
" The next import is defined only for test"
import libevents.events as Events

import libutils.gnscheduler as Scheduler


class SchedEvToFr(Scheduler.Scheduler):
    '''Subclass of Scheduler for adapting layer 1 and 2.
    '''

    def fn_sched(self):
        '''Scheduling function to process  events queue, generates frames and put the frames in the output queue.
        
        Reads one element from the input event queue, generates a frame, and put the frame in  the output queue.
        out_queues: a dictionary. 
        '''
        in_qu = self.in_queues[0]
        event = in_qu.get(True)
        #print 'event', event
        frame= events.mkframe(event)
        out_queue = self.out_queues['frames']
        out_queue.put(frame, False)   # add to queue, don't block 
        #print " out queue size ", out_queue.qsize()
        in_qu.task_done()        
 


def test():
    '''Tests on frames.

    Frames are put in output queue.
    '''
    frame_q = Queue.Queue(10)
    ev_q = Queue.Queue(10)
    
    out_queues = { \
        'frames':    (frame_q) \
    }
    sch = SchedEvToFr(ev_q, out_queues)
    
 
    # put events in input queue
    for name in ['MgmtBeacon', 'CtrlRTS', 'CtrlCTS', 'DataData']:
        ev = Events.mkevent(name)
        ev.src_addr = "100"
        ev.dst_addr=  "150"
        print " Event = ", ev
        ev_q.put(ev,False)
    print 'Input queue size', ev_q.qsize()

    # create and start scheduler
    print '\n=== Process ==='
    sch.start()
    ev_q.join()
    sch.stop()
    sch.join()   
  

    print '\n=== Read the output queue ==='
    print 'Queue size:', frame_q.qsize()
    while not frame_q.empty():
        item = frame_q.get()
        print "Frame ", item
   
  
    return
    
    


if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        sys.exit()

