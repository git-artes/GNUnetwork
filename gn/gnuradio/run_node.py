#!/usr/bin/env python
#
# Copyright 2010,2011 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 
import sys
sys.path +=['..']
from gnuradio import gr
from gnuradio.eng_option import eng_option
from optparse import OptionParser

# From gr-digital
from gnuradio import digital

# from current dir
from transmit_path import transmit_path as tp36
from transmit_path import transmit_path as tp37

from uhd_interface import uhd_transmitter

from receive_path import receive_path as rp36
from receive_path3_7 import receive_path as rp37
from uhd_interface import uhd_receiver
import TxRxLayer1
import time, struct, sys, threading,Queue
import libmanagement.NetworkConfiguration as NetworkConfiguration
import libmanagement.DiscoveryPeeringController as DiscoveryPeeringController
import libmanagement.Beacon as Beacon
import libadaptationlayer.schedEvToFr as schedEvToFr
import libadaptationlayer.schedFrToEv as schedFrToEv

        

# /////////////////////////////////////////////////////////////////////////////
#                                   main
# /////////////////////////////////////////////////////////////////////////////

class StartL2():

    def __init__(self, q_rx,q_tx,mac_addr):
        self.q_rx =q_rx
        self.q_tx = q_tx
        self.mac_addr = mac_addr
        self.isrunning = False
        return

    def start(self):
        self.isrunning = True
        " Configuration of the Scheduler of Node 1 that recieves frames and generates management events."
        frame_rx_q1 = self.q_rx
        ctrl_q1, mgmt_q1, data_q1 = Queue.Queue(10), Queue.Queue(10), Queue.Queue(10)
        out_queues1 = { \
            'Ctrl': (ctrl_q1), \
            'Mgmt': (mgmt_q1), \
            'Data': (data_q1)  \
            }
        self.sch1 = schedFrToEv.SchedFrToEv(frame_rx_q1, out_queues1)
        self.sch1.start()
        
        "Configuration of the scheduler of Node 1 that recieves events and generates frame events."
        frame_tx_q1 = self.q_tx
        tx_ev_q1 = Queue.Queue(10)
        out_queues_tx1 = { \
            'frames':    (frame_tx_q1) \
        }
        self.tx1 = schedEvToFr.SchedEvToFr(tx_ev_q1, out_queues_tx1)
        self.tx1.start()

        " Network configuration: the MAC Addr, the name of the network and the broadcast Addr"    
        net_conf1 = NetworkConfiguration.NetworkConfiguration(self.mac_addr,'my network',"256")
        net_conf1.retry_timeout = 5    
        " Starts the Controller of The FSM for Peering Discovering"
        self.dpcontrol1 =  DiscoveryPeeringController.DiscoveryPeeringController(net_conf1,None,mgmt_q1,tx_ev_q1)
        self.dpcontrol1.start()
        "Starts the beacon generator of this node"
        self.myBeacon1 = Beacon.Beacon(net_conf1 ,tx_ev_q1)
        self.myBeacon1.start()          

    def stop(self):
         if self.isrunning == True:
             self.sch1.stop()     
             self.tx1.stop()
             self.dpcontrol1.stop()
             self.myBeacon1.stop()
             self.isrunning = False

class StartL1():

    def __init__(self, q_rx,q_tx,options,modulator,demodulator):
       
        self.q_rx =q_rx
        self.q_tx = q_tx
        self.options = options
        self.demodulator =demodulator
        self.modulator = modulator
        return

    def start(self):

   
        if self.options.receive != 0:
            self.tb_rx = TxRxLayer1.my_top_block_rx(self.demodulator, self.options,self.q_rx)
            self.tb_rx.start()        # start flow graph
            if self.options.testL1 != 0:
                self.test_rx=TestLayer1Rx(self.q_rx,self.options)
                self.test_rx.start()
    
        if self.options.transmit != 0:
            self.tb = TxRxLayer1.my_top_block_tx(self.modulator, self.options,self.q_tx)
            self.tb.start() 
            if self.options.testL1 != 0:
                self.test=TestLayer1Tx(self.q_tx,self.options)
                self.test.start()
    def set_rx_freq(self,value):            
        self.tb_rx.set_freq(value)

    def set_tx_freq(self,value):            
        self.tb.set_freq(value)

    def sense_carrier(self):
        self.tb_rx.sense_carrier()


    def stop(self):
        self.tb.tx_l1.stop()
        if self.options.testL1 != 0:
            self.test.stop()
            self.test_rx.stop()
        self.tb.stop()
        self.tb.wait()   
        print("tx top block stopped")
        self.tb_rx.stop()                    # wait for it to finis
        self.tb_rx.wait()         # wait for it to finish
        print("rx top block stopped")

class TestLayer2Tx(threading.Thread) :
    
    def __init__(self,q_tx,options,l1):
 
        threading.Thread.__init__(self)
        self.q_tx =q_tx
        self.finished = False
        self.options =options
        self.l1=l1
    def run(self):
        while not self.finished:
            c = raw_input('Press #z to end, or #,cmd to test commands :')        
            while c != "#z":
                try:
                    a1,a2,a3 = c.split(',',2)
                    if a1== '#':
                        if a2=='snd':
                            self.q_tx.put(a3)
                        else: 
                            if a2== 'rx_freq':
                                print " ready to set the new frequency"
                                self.l1.set_rx_freq(float(a3))       
                                print " New Rx frequency ", a3
                            else: 
                                if  a2== 'tx_freq':       
                                     self.l1.set_tx_freq(float(a3))
                                     print " New Tx frequency ", a3
                                else: 
                                    if  a2== 'sense':
                                        print " Sensing ...."
                                        self.l1.sense_carrier()
                except:
                    pass
                c = raw_input('Press #z to end, or #,cmd to test commands :')        
                    
            self.stop()
         
    def stop(self):
        self.finished=True
        self._Thread__stop()

class TestLayer2Rx(threading.Thread) :
  
    def __init__(self,q_rx,options):
   
        threading.Thread.__init__(self)
        self.q_rx =q_rx
        self.finished = False
        self.options =options
        
    def run(self):
        while not self.finished:
            payload = self.q_rx.get()
            print payload
                
    def stop(self):
        self.finished=True
        self._Thread__stop()


class TestLayer1Tx(threading.Thread) :
    
    def __init__(self,q_tx,options):
 
        threading.Thread.__init__(self)
        self.q_tx =q_tx
        self.finished = False
        self.options =options
    def run(self):
        print "run....."
        while not self.finished:
            nbytes = int(1e6 * self.options.megabytes)
            n = 0
            pktno = 0
            pkt_size = int(self.options.size)
        
            while n < nbytes and self.finished==False:
                data = (pkt_size - 2) * chr(pktno & 0xff) 
                payload = struct.pack('!H', pktno & 0xffff) + data
                self.q_tx.put(payload)
                n += len(payload)
                print "#"
                time.sleep(1)
                if self.options.discontinuous and pktno % 5 == 4:
                    time.sleep(1)
                pktno += 1
            print("TestL2 ends")                
                
    def stop(self):
        self.finished=True
        self._Thread__stop()


class TestLayer1Rx(threading.Thread) :
  
    def __init__(self,q_rx,options):
   
        threading.Thread.__init__(self)
        self.q_rx =q_rx
        self.finished = False
        self.options =options
        self.n_rcvd =0
        self.n_right= 0
        
    def run(self):
        print "run rx ...."
        while not self.finished:
            payload = self.q_rx.get()
            (pktno,) = struct.unpack('!H', payload[0:2])
            self.n_rcvd += 1
            self.n_right += 1
            print "pktno = %4d  n_rcvd = %4d  n_right = %4d" % (
            pktno, self.n_rcvd, self.n_right)           
                
    def stop(self):
        self.finished=True
        self._Thread__stop()


def main():
    mods = digital.modulation_utils.type_1_mods()
    demods = digital.modulation_utils.type_1_demods()
    parser = OptionParser(option_class=eng_option, conflict_handler="resolve")
    expert_grp = parser.add_option_group("Expert")

    parser.add_option("-m", "--modulation", type="choice", choices=mods.keys(),
                      default='bpsk',
                      help="Select modulation from: %s [default=%%default]"
                            % (', '.join(mods.keys()),))

    parser.add_option("-s", "--size", type="eng_float", default=100,
                      help="set packet size [default=%default]")
    parser.add_option("-M", "--megabytes", type="eng_float", default=1.0,
                      help="set megabytes to transmit [default=%default]")
    parser.add_option("","--discontinuous", action="store_true", default=False,
                      help="enable discontinous transmission (bursts of 5 packets)")
    parser.add_option("","--from-file", default=None,
                      help="use intput file for packet contents")
    parser.add_option("","--to-file", default=None,
                      help="Output file for modulated samples")
    parser.add_option("", "--receive", type="int", default=1 , help = "if the USRP receive or only transmit")
    parser.add_option("", "--transmit", type="int", default=1 , help = "if the USRP transmit or only receive")
    parser.add_option("", "--testL1", type="int", default=0 , help = "if MAC is used (default=0) or not (1)")
    parser.add_option("", "--mac", default=None , help = "MAC addres")
    parser.add_option("", "--command", default=0 , help = "Command mode")
    parser.add_option("", "--version", default=6 , help = "gnuradio version, default 6 (3.6)")
     
    tp36.add_options(parser, expert_grp)
    tp37.add_options(parser, expert_grp)

    uhd_transmitter.add_options(parser)
  
    rp36.add_options(parser, expert_grp)
    rp37.add_options(parser, expert_grp)
    uhd_receiver.add_options(parser)

    for mod in demods.values():
        mod.add_options(expert_grp)
    for mod in mods.values():
        mod.add_options(expert_grp)
    (options, args) = parser.parse_args ()
    if len(args) != 0:
        parser.print_help()
        sys.exit(1)           
    if options.from_file is not None:
        source_file = open(options.from_file, 'r')
    r = gr.enable_realtime_scheduling()
    if r != gr.RT_OK:
        print "Warning: failed to enable realtime scheduling"
    q_tx =Queue.Queue(10)
    q_rx =Queue.Queue(10) 
    l1=StartL1(q_rx,q_tx,options,mods[options.modulation],demods[options.modulation])
    l1.start()
    if options.testL1 == 0 and options.command ==0:
        l2 = StartL2(q_rx,q_tx,options.mac)
        l2.start()
    c = raw_input('Press #z to end, or #w to test commands :')        
    while c != "#z":
       if c== "#w" and options.command !=0:
         print "Enter command mode... ", options.command  
         testl2tx= TestLayer2Tx(q_tx,options,l1)          
         testl2tx.start()
         testl2rx = TestLayer2Rx(q_rx,options)
         testl2rx.start()
         testl2tx.join()
         testl2rx.stop()
       c = raw_input('Press #z to end, or #w to test commands :')        
           
    print "Program ends"
    l1.stop()
    if options.testL1 == 0 and options.command ==0:
        l2.stop()
    exit(0)
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
