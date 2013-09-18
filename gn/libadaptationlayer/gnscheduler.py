#!/usr/bin/env python
# -*- coding: utf-8 -*-

# scheduler: a generic scheduler

'''Classes and Functions to implement a generic scheduler.
'''

import threading  #, Queue


class Scheduler(threading.Thread):
    '''Extracts elements from an input queue, adds elements to output queues.
    
    This scheduler extracts elements from an input queue, and according to the element type applies a procedure, eventually creates other elements of potentially different types, and places them in one or more output queues.
    '''
    def __init__(self, in_queue, dc_outqueues):
        '''Constructor.
        
        @param in_queue: the input queue from which items are extracted. Items in the input queue must contain a function getname() to classify.
        @param dc_outqueues: a dictionary of {item_type: (function, output_queue)}. The item_type is a string; the function returns an element to put in the output queue.
        '''
        threading.Thread.__init__(self)
        self.daemon = True
        self.finished = False
        self.in_queue = in_queue
        self.dc_outqueues = dc_outqueues

    def run(self):
        '''Runs the scheduler until stopped.
        '''
        while not self.finished:
            if not self.in_queue.empty():
                in_item = self.in_queue.get()
                for item_type in self.dc_outqueues.keys():
                    if in_item.getname() == item_type:
                        # function to execute, output queue
                        fn_in_item, out_queue = self.dc_outqueues[item_type]
                        out_item = fn_in_item(in_item)   # exec fn, make out_item
                        out_queue.put(out_item, False)   # add to queue, don't block 
                        break
                else:
                    print 'Scheduler, item type not recognized:', in_item.getname()
                self.in_queue.task_done()

            else:
                print 'input queue empty!'   # shows sometimes...
        else:
            print 'Scheduler, stopped'
            self.stop()
        self.in_queue.join()
        return


    def stop(self):
        '''Stops the scheduler.
        '''
        print 'Scheduler, in stop function'
        self.finished = True
        self._Thread__stop()



