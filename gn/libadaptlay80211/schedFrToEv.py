#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sched-bytype.py
#


'''A frame to event scheduler, based on IEEE 802.11 frames.

A scheduler that gets a frame from a Layer 1 input queue, generates the corresponding event, and puts it into Management, Control or Data queues based on the event type.
'''

import Queue
import sys
sys.path +=['..']

import libutils.gnscheduler as gnscheduler
import libevents.if_events as if_events
import libframes.if_frames as if_frames



class SchedFrToEv(gnscheduler.Scheduler):
    '''Subclass of Scheduler for adapting layers 1 and 2.
    '''

    def fn_sched(self):
        '''Scheduling function, reads frames, outputs events by type.
        
        Scheduler function to process a frames queue: reads one element from the input frame queue, generates an event, and puts the event in one of the output queues according to its type.
        
        out_queues: a dictionary of {nm_queue: (out_queue)}; nm_queue is a name for the queue, out_queue is the output queue.
        '''
        in_qu = self.in_queues[0]
        frame = in_qu.get(True)
        print " recibi frame : ", repr(frame)
        frm_obj = if_frames.objfrompkt(frame)
        event = if_events.frmtoev(frm_obj)
        print "recibi event : ", event
        if event != None:
            for item_type in self.out_queues.keys():
                if  event.ev_type == item_type:
                    # function to execute, output queue
                    out_queue = self.out_queues[item_type]
                    out_queue.put(event, False)   # add to queue, don't block 
                    break
            else:
                raise if_events.EventFrameException('Scheduler, event type \
                    not recognized: ', event.ev_type)
        else:
                raise if_events.EventFrameException('Scheduler, error in \
                    frame')
        in_qu.task_done()
        return



if __name__ == '__main__':
    import doctest
    testfilename = sys.argv[0][:-2] + 'txt'
    try:
        doctest.testfile(testfilename)
    except:      # no text file present
        pass



