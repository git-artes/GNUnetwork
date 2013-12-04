#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# schedEvToFr.py
#


'''An event to frame scheduler, from Layer 2 into Layer 1.

A scheduler that gets an event from a Layer 2 input queue, generates the corresponding frame, and puts it into the Layer 1 transmit queue.
'''
import Queue
import sys

sys.path +=['..']

import libutils.gnscheduler as Scheduler

# The next import is defined only for testing
import libevents.evstrframes as evstrframes
#import libevents.events as Events
import libevents.if_events as if_events


class SchedEvToFr(Scheduler.Scheduler):
    '''Subclass of Scheduler for adapting Layers 1 and 2.
    '''

    def fn_sched(self):
        '''Scheduling function to process an events queue.
        
        Scheduling function to process an events queue: reads one element from the input event queue, generates a frame, and puts this frame in  the output queue.
        out_queues: a dictionary. 
        '''
        in_qu = self.in_queues[0]
        event = in_qu.get(True)
        #print 'SchedEvToFr, event', event
        frame = evstrframes.mkframe(event)
        out_queue = self.out_queues['frames']
        out_queue.put(frame, False)   # add to queue, don't block 
        #print " out queue size ", out_queue.qsize()
        in_qu.task_done()



def test():
    '''Tests SchedEvToFr class.

    Put some events in input queue to read, create frames and put in output queue.
    '''
    frame_q = Queue.Queue(10)
    ev_q = Queue.Queue(10)
    
    out_queues = { \
        'frames':    (frame_q) \
    }
    sch = SchedEvToFr(ev_q, out_queues)
    
 
    # create events and put in input queue
    for name in ['MgmtBeacon', 'CtrlRTS', 'CtrlCTS', 'DataData']:
        #ev = if_events.mkevent(name, ev_dc={'src_addr':'100','dst_addr':'150'})
        ev = if_events.mkevent(name, ev_dc={'src_addr':'100','dst_addr':'150'})
        print ev
        ev_q.put(ev, False)
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

