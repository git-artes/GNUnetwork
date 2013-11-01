#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sched-bytype.py
#


'''An scheduler that get a frame from Layer 1 input queue, generates the corresponding event, and put it into the Management, Control or Data queues based on the event type .
'''
import Queue
import sys
sys.path +=['..']
import libevents.if_events as events
" The next import is defined only for test"
import libevents.events as Events

import libutils.gnscheduler as Scheduler


class SchedFrToEv(Scheduler.Scheduler):
    '''Subclass of Scheduler for adapting layer 1 and 2.
    '''

    def fn_sched(self):
        '''Scheduling function to process  frames queue, generates events and put the events in the output queue according to it type.
        
        Reads one element from the input frame queue, generates an event, and put the event in one of the output queue according to it type.
        out_queues: a dictionary of {nm_queue: (out_queue)}. 
        '''
        in_qu = self.in_queues[0]
        if not in_qu.empty():
            frame = in_qu.get()
            event= events.mkevent(pframe=frame)
            for item_type in self.out_queues.keys():
                if  event.ev_type == item_type:
                    # function to execute, output queue
                    out_queue = self.out_queues[item_type]
                    out_queue.put(event, False)   # add to queue, don't block 
                    break
            else:
                print 'Scheduler, event type not recognized:', event.ev_type
            in_qu.task_done()
        else:
            print 'input queue empty!'   # shows sometimes...
        return



def test():
    '''Tests on frames.

    Events are put in output queues according to their type.
    '''
    frame_q = Queue.Queue(10)
    ctrl_q, mgmt_q, data_q = Queue.Queue(10), Queue.Queue(10), Queue.Queue(10)
    ls_out_queues = [ctrl_q, mgmt_q, data_q]
    out_queues = { \
        'Ctrl': (ctrl_q), \
        'Mgmt': (mgmt_q), \
        'Data': (data_q)  \
        }



    sch = SchedFrToEv(frame_q, out_queues)
    

    # create input queue
 
    # put events in input queue
    for name in ['MgmtBeacon', 'CtrlRTS', 'CtrlCTS', 'DataData']:
        ev = Events.mkevent(name)
        ev.src_addr = "100"
        ev.dst_addr=  "150"
        frame=events.mkframe(ev)
        print " Frame = ", frame
        frame_q.put(frame,False)
    print '=== Scheduler based on item type ==='
    print 'Input queue size', frame_q.qsize()

    # create and start scheduler
    print '\n=== Process ==='
    sch.start()
    frame_q.join()
    sch.stop()
    sch.join()

    print '\n=== Read the output queues ==='
    for qu in ls_out_queues:
        print 'Queue size:', qu.qsize()
        while not qu.empty():
            item = qu.get()
            print "Event", item
    return
    
    


if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        sys.exit()

