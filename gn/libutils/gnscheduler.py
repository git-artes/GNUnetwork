#!/usr/bin/env python
# -*- coding: utf-8 -*-

# scheduler: a generic scheduler

'''Classes and Functions to implement a generic scheduler.
'''

import threading


class Scheduler(threading.Thread):
    '''Gets elements from input queues, processes, puts elements in output queues.
    
    This scheduler gets one element from one of several input queues, and puts elements in one or several output queues. Behaviour is regulated by a scheduling function which is expected to be overwritten when subclassing this class. Selection of input queue to get element from, processing, creation of one or more elements of same or different type, and putting elements in output queues are all regulated by this scheduling function.
    '''
 
    def __init__(self, in_queues, out_queues):
        '''Constructor.
        
        @param in_queues: a list of input queues from which items are extracted. If input queues are given within a more elaborate structure, functin run() must be overwritten.
        @param out_queues: a structure containing the output queues. A possible structure is a dictionary of key nm_queue, the name of an output queue; value may be a queue, a tuple (function, queue) or other structure to be processed by the scheduling function fn_sched, which must be overwritten.
        '''
        threading.Thread.__init__(self)
        self.daemon = True
        self.finished = False
        if type(in_queues) is list:        # accept a list of queues, or a single queue
            self.in_queues = in_queues
        else:
            self.in_queues = [in_queues]
        self.out_queues = out_queues    # output queues in a dictionary
        return

    def fn_sched(self):
        '''A dummy scheduling function; to be overwritten in a subclass.
        '''
        pass
        return


    def run(self):
        '''Runs the scheduler until stopped.
        '''
        while not self.finished:
            self.fn_sched()
        else:
            #print 'Scheduler, stopped'
            self.stop()
        for in_qu in self.in_queues:
            in_qu.join()
        return


    def stop(self):
        '''Stops the scheduler.
        '''
        print 'Scheduler, in stop function'
        self.finished = True
        self._Thread__stop()



