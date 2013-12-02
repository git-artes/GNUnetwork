#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sched-bytype.py
#


'''A frame to event scheduler, from Layer 1 into Layer 2.

A scheduler that gets a frame from a Layer 1 input queue, generates the corresponding event, and puts it into Management, Control or Data queues based on the event type.
'''
import Queue
import sys
sys.path +=['..']
import libevents.evstrframes as evstrframes
# The next import is defined only for test
import libevents.if_events as if_events

import libutils.gnscheduler as Scheduler


class SchedFrToEv(Scheduler.Scheduler):
    '''Subclass of Scheduler for adapting layers 1 and 2.
    '''

    def fn_sched(self):
        '''Scheduling function, reads frames, outputs evstrframes by type.
        
        Reads one element from the input frame queue, generates an event, and puts the event in one of the output queues according to its type.
        out_queues: a dictionary of {nm_queue: (out_queue)}; nm_queue is a name for the queue, out_queue is the output queue.
        '''
        in_qu = self.in_queues[0]
        frame = in_qu.get(True)
        event = evstrframes.mkevent(pframe=frame)
        if event != None:
            for item_type in self.out_queues.keys():
                if  event.ev_type == item_type:
                    # function to execute, output queue
                    out_queue = self.out_queues[item_type]
                    out_queue.put(event, False)   # add to queue, don't block 
                    break
            else:
                print 'Scheduler, event type not recognized:', event.ev_type
        else:
            print "Scheduler, erroneous frame"
        in_qu.task_done()
        return



def test():
    '''Tests SchedFrToEv class.

    Put some frames in input queue to read, creates events and puts in different output queues according to the event type.
    '''

    # create input queue
    frame_q = Queue.Queue(10)
    ctrl_q, mgmt_q, data_q = Queue.Queue(10), Queue.Queue(10), Queue.Queue(10)
    ls_out_queues = [ctrl_q, mgmt_q, data_q]
    out_queues = { \
        'Ctrl': (ctrl_q), \
        'Mgmt': (mgmt_q), \
        'Data': (data_q)  \
        }
    sch = SchedFrToEv(frame_q, out_queues)

    # put events in input queue
    for name in ['MgmtBeacon', 'CtrlRTS', 'CtrlCTS', 'DataData']:
        ev = if_events.mkevent(name, ev_dc={'src_addr':'100','dst_addr':'150'})
        frame = evstrframes.mkframe(ev)
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

