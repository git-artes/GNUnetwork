#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# schedone.py
#


'''An example scheduler based on item types.
'''

import sys
sys.path += ['..']
import Queue

from gnscheduler import Scheduler


class SchedOne(Scheduler):

    def fn_sched(self):
        '''Scheduling function to process queue elements acording to type.
        
        Reads one element from one of the input queues, examines element, acts according to its type, as stated in dc_outqueues.
        dc_outqueues: a dictionary of {nm_queue: (fn_queue, out_queue)}. The item_type is a string; the function returns an element to put in the output queue.
        '''
        in_qu = self.in_queues[0]
        if not in_qu.empty():
            in_item = in_qu.get()
            for item_type in self.dc_outqueues.keys():
                if in_item.getname() == item_type:
                    # function to execute, output queue
                    fn_in_item, out_queue = self.dc_outqueues[item_type]
                    out_item = fn_in_item(in_item)   # exec fn, make out_item
                    out_queue.put(out_item, False)   # add to queue, don't block 
                    break
            else:
                print 'Scheduler, item type not recognized:', in_item.getname()
            in_qu.task_done()
        else:
            print 'input queue empty!'   # shows sometimes...
        return




class Item:
    def __init__(self, name):
        self.name = name
    def getname(self):
        return self.name
    def __str__(self):
        return '  item: ' + self.name


def fn_item(item):
    print 'fn_item: do some work; item:', item
    return item


def test():
    '''Tests on items.
    '''
    ctrl_q, mgmt_q, data_q = Queue.Queue(10), Queue.Queue(10), Queue.Queue(10)
    dc_outqueues = { \
        'CtrlRTS':    (fn_item, ctrl_q), \
        'CtrlCTS':    (fn_item, ctrl_q), \
        'MgmtBeacon': (fn_item, mgmt_q), \
        'DataData':   (fn_item, data_q)  \
        }

    # create input queue
    frame_q = Queue.Queue(10)

    # put events in input queue
    for name in ['MgmtBeacon', 'CtrlRTS', 'CtrlCTS', 'DataData']:
        item = Item(name)
        frame_q.put(Item(name))
    print '=== Scheduler based on item type ==='
    print 'Input queue size', frame_q.qsize()

    # create and start scheduler
    sch = SchedOne(frame_q, dc_outqueues)
    
    print '\n=== Process ==='
    sch.start()
    frame_q.join()
    sch.stop()
    sch.join()

    print '\n=== Read the output queues ==='
    for nm in dc_outqueues.keys():
        (fn, qu) = dc_outqueues[nm]
        print 'Queue:', nm, '; size:', qu.qsize()
        while not qu.empty():
            item = qu.get()
            print item

    return
    


if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        sys.exit()

