#!/usr/bin/env python
# -*- coding: utf-8 -*-

# schedulertest: test of generic scheduler using events

import Queue

from gnscheduler import Scheduler

import sys
sys.path += ['..']


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
    print '=== Scheduler, testing ==='
    print 'Input queue size', frame_q.qsize()

    # create and start scheduler
    sch = Scheduler(frame_q, dc_outqueues)
    
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

