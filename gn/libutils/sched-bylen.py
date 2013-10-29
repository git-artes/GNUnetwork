#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sched-bylen.py
#


'''An example scheduler based on item types.
'''

import sys
sys.path += ['..']
import Queue
import time

from gnscheduler import Scheduler


class SchedShort(Scheduler):
    '''Subclass of Scheduler for output on shortest queue.
    '''

    def getshortest(self):
        '''Returns queue of shortest length.
        '''
        qu_short = self.out_queues[0]
        print '  queue sizes: ',
        for out_qu in self.out_queues:
            print out_qu.qsize(), 
            if out_qu.qsize() < qu_short.qsize():
                qu_short = out_qu
        print '; qu_shortest:', qu_short.qsize()
        return qu_short


    def fn_sched(self):
        '''Gets items from input queues, puts on shortest output queue.
        
        Reads one element from one of the input queues, shows value (other work may be done), puts on shortest of output queues.
        '''
        for in_qu in self.in_queues:
            if not in_qu.empty():
                in_item = in_qu.get()
                print 'Item', in_item, ';',
                out_qu_short = self.getshortest()      # shortest output queue, now
                out_item = in_item                     # or do something
                out_qu_short.put(out_item, False)      # add to queue, don't block 
                in_qu.task_done()
                time.sleep(1)

            else:
                print 'Input queue empty'
        #else:
        #    print 'All input queues empty!'   # shows sometimes...
        return


def test():
    '''Tests on items.
    '''

    inqu_a, inqu_b = Queue.Queue(), Queue.Queue()
    for it in ['a'+str(i) for i in range(1, 16)]:
        inqu_a.put(it)
    for it in ['b'+str(i) for i in range(1, 12)]:
        inqu_b.put(it)
    in_queues = [inqu_a, inqu_b]
        
    outqu_1, outqu_2, outqu_3 = Queue.Queue(), Queue.Queue(), Queue.Queue()
    for it in ['o'+str(i) for i in range(1, 5)]:
        outqu_2.put(it)
    for it in ['p'+str(i) for i in range(1, 2)]:
        outqu_3.put(it)
    out_queues = [outqu_1, outqu_2, outqu_3]

    print '\nInput queues, sizes:',
    for qu in in_queues:
        print qu.qsize(),
    print
    print '\nOutput queues, sizes:',
    for qu in out_queues:
        print qu.qsize(),
    print

    sch = SchedShort(in_queues, out_queues)
    
    print '\n=== Process ==='
    sch.start()
    #frame_q.join()
    for qu in in_queues:
        qu.join()
    sch.stop()
    sch.join()


    print '\n=== Read the output queues ==='
    for qu in out_queues:
        print '-- Out queue, size:', qu.qsize(), '\n  ',
        while not qu.empty():
            item = qu.get()
            print item,
        print

    return
    


if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        sys.exit()

