#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sched-bytype.py
#


'''A layer 3 to layer 2 scheduler.

A scheduler that gets an event from a Layer 3 input queue, generate a corresponding event, and puts it into the Layer 2 queue.
WARNING. We now asume that the events generated by L3 are the same of those of L2, so for the moment this scheduler is only a gateway that takes the events from the input queue and puts the same events in the output queue.
'''
import Queue
import sys
sys.path +=['..']

# The next import is defined only for test
import libevents.if_events as if_events

import libutils.gnscheduler as Scheduler

import os,struct,threading

# ////////////////////////////////////////////////////////////////////
#
#   Use the Universal TUN/TAP device driver to move packets to/from
#   kernel
#
#   See /usr/src/linux/Documentation/networking/tuntap.txt
#
# ////////////////////////////////////////////////////////////////////

# Linux specific...
# TUNSETIFF ifr flags from <linux/tun_if.h>

IFF_TUN		= 0x0001   # tunnel IP packets
IFF_TAP		= 0x0002   # tunnel ethernet frames
IFF_NO_PI	= 0x1000   # don't pass extra packet info
IFF_ONE_QUEUE	= 0x2000   # beats me ;)

def open_tun_interface(tun_device_filename):
    from fcntl import ioctl
    
    mode = IFF_TAP | IFF_NO_PI
    TUNSETIFF = 0x400454ca

    tun = os.open(tun_device_filename, os.O_RDWR)
    ifs = ioctl(tun, TUNSETIFF, struct.pack("16sH", "gr%d", mode))
    ifname = ifs[:16].strip("\x00")
    return (tun, ifname)
    
class Layer3:
    '''Subclass of Scheduler for adapting layers 3 and 2.
    '''
    
    def __init__(self,out_queue,in_queue, device,my_addr,dst_addr):
        '''  
        Constructor
        
        @param mgmt_queue : The queue to put the management events.
        '''
        self.my_addr = my_addr
        self.dst_addr = dst_addr
        self.out_queue = out_queue
        self.in_queue = in_queue
        self.device = device
        (self.tun_fd, self.tun_ifname) = open_tun_interface(device)
        self.finished = False
        print
        print "Allocated virtual ethernet interface: %s" % (self.tun_ifname,)
        print "You must now use ifconfig to set its IP address. E.g.,"
        print
        print "  $ sudo ifconfig %s 192.168.200.1" % (self.tun_ifname,)
        print
        print "Be sure to use a different address in the same subnet for each machine."
        print
        self.sch = ReadLayer3(out_queue,self.tun_fd,self.my_addr,self.dst_addr)
        self.sch2 = ReadLayer2(in_queue,self.tun_fd)        
        self.sch.start()
        self.sch2.start()
        
    def stop(self):        
        self.sch.stop()
        self.sch2.stop()
        
        
class ReadLayer3(threading.Thread):
    '''Subclass of Scheduler for adapting layers 3 and 2.
    '''
    
    def __init__(self,out_queue,tun_fd,my_addr,dst_addr):
        '''  
        Constructor
        
        @param mgmt_queue : The queue to put the management events.
        '''
        threading.Thread.__init__(self)
        self.my_addr = my_addr
        self.dst_addr = dst_addr
        self.out_queue = out_queue
        self.tun_fd = tun_fd
        self.finished = False

        
        
        
    def run(self):
        '''Scheduling function, reads events, outputs events.
        
        Reads one element from the input event queue, and puts the event in the output queue.
        out_queues: a dictionary of {nm_queue: (out_queue)}; nm_queue is a name for the queue, out_queue is the output queue.
        '''
        print "start..........................."     
        while not self.finished :
            payload = os.read(self.tun_fd, 10*1024)
            if not payload:
                print "No payload"
            else:
                print "Tx: len(payload) = %4d" % (len(payload),)       
                event = if_events.mkevent("DataData")
                event.ev_dc['src_addr'] = self.my_addr
                event.ev_dc['dst_addr'] = self.dst_addr
                event.ev_dc['payload'] = payload
                self.out_queue.put(event, False)   # add to queue, don't block         
            
        return
    def stop(self):
        self.finished = True
        self._Thread__stop()

class ReadLayer2(threading.Thread):
    '''Subclass of Scheduler for adapting layers 3 and 2.
    '''
    
    def __init__(self,in_queue,tun_fd):
        '''  
        Constructor
        
        @param mgmt_queue : The queue to put the management events.
        '''
        threading.Thread.__init__(self)
        self.in_queue = in_queue
        self.tun_fd = tun_fd
        self.finished = False
        
        
    def run(self):
        '''Scheduling function, reads events, outputs events.
        
        Reads one element from the input event queue, and puts the event in the output queue.
        out_queues: a dictionary of {nm_queue: (out_queue)}; nm_queue is a name for the queue, out_queue is the output queue.
        '''
        while not self.finished :
            event = self.in_queue.get()
            payload = event.ev_dc['payload']
            print "Rx:  len(payload) = %4d" % (len(payload))
            os.write(self.tun_fd, payload)
        return
    def stop(self):
        self.finished = True
        self._Thread__stop()
def test():
    '''Tests the SchedLayer3 subclass.

    Puts some events in input queue, runs scheduler, puts events in output queue.
    '''

    # create input queue
    layer3_q = Queue.Queue(10)
    layer2_q = Queue.Queue(10)

    l3= Layer3(layer3_q,layer3_q,'/dev/net/tun',100,200)
    c = raw_input('Press #z to end, or #w to test commands :')        
    while c != "#z":
       c = raw_input('Press #z to end, or #w to test commands :')        
    l3.stop()       
    print "Program ends"

    # put events in input queue
#    for i in range(1, 5) :
#        ev = if_events.mkevent('DataData', \
#            ev_dc={'src_addr':'100','dst_addr':'150'})
#        print ev
#        layer3_q.put(ev,False)
#    print 'Input queue size', layer3_q.qsize()

    # create and start scheduler


    
    #layer3_q.join()
    #sch.stop()
    #sch.join()

#    print '\n=== Read the output queues ==='
#    print 'Queue size:', layer2_q.qsize()
#    while not layer2_q.empty():
#        item = layer2_q.get()
#        print "Event", item
    return
    
    


if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        sys.exit()

