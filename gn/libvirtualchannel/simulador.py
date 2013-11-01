# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:55:46 2013

@author: belza
"""

import sys
sys.path +=['..']

import Queue
import libmanagement.NetworkConfiguration as NetworkConfiguration
import libmanagement.DiscoveryPeeringController as DiscoveryPeeringController
import libmanagement.Beacon as Beacon
import libadaptationlayer.scheduler as scheduler
import libadaptationlayer.transmitFrame as transmitFrame
import virtualchannel


def simulates():
    "-------------------NODO 100-------------------------------------------------------"    
    frame_rx_q1 = Queue.Queue(10)
    frame_tx_q1 = Queue.Queue(10)
    ctrl_q1 = Queue.Queue(10)
    mgmt_q1 = Queue.Queue(10)
    data_q1 = Queue.Queue(10)
    tx_ev_q1= Queue.Queue(10)
    sch1 = scheduler.Scheduler(frame_rx_q1,ctrl_q1,data_q1,mgmt_q1)
    sch1.start()
    tr1 = transmitFrame.TransmitFrame(frame_tx_q1,tx_ev_q1)
    tr1.start()
    net_conf1 = NetworkConfiguration.NetworkConfiguration("100",'my network',"256",1)
    net_conf1.retry_timeout = 5    
    dpcontrol1 =  DiscoveryPeeringController.DiscoveryPeeringController(net_conf1,None,mgmt_q1,tx_ev_q1)
    dpcontrol1.start()
    myBeacon1 = Beacon.Beacon(net_conf1 ,tx_ev_q1)
    myBeacon1.start()    
    "---------------------FIN NODO 100 -----------------------------------------------"
#    
    
    "-------------------NODO 102-------------------------------------------------------"    
    frame_rx_q2 = Queue.Queue(10)
    " En el simulador todos escriben los paquetes a la misma cola del canal virtual"
    frame_tx_q2 = frame_tx_q1 
    ctrl_q2 = Queue.Queue(10)
    mgmt_q2 = Queue.Queue(10)
    data_q2 = Queue.Queue(10)
    tx_ev_q2= Queue.Queue(10)
    sch2 = scheduler.Scheduler(frame_rx_q2,ctrl_q2,data_q2,mgmt_q2)
    sch2.start()
    tr2 = transmitFrame.TransmitFrame(frame_tx_q2,tx_ev_q2)
    tr2.start()
    net_conf2 = NetworkConfiguration.NetworkConfiguration("102",'my network',"256",1)
    net_conf2.retry_timeout = 5    
    dpcontrol2 =  DiscoveryPeeringController.DiscoveryPeeringController(net_conf2,None,mgmt_q2,tx_ev_q2)
    dpcontrol2.start()
    myBeacon2 = Beacon.Beacon(net_conf2 ,tx_ev_q2)
    myBeacon2.start()    
    "---------------------FIN NODO 101 -----------------------------------------------"

 
    "-------------------NODO 102-------------------------------------------------------"    
    frame_rx_q3 = Queue.Queue(10)
    " En el simulador todos escriben los paquetes a la misma cola del canal virtual"
    frame_tx_q3 = frame_tx_q2 
    ctrl_q3 = Queue.Queue(10)
    mgmt_q3 = Queue.Queue(10)
    data_q3 = Queue.Queue(10)
    tx_ev_q3= Queue.Queue(10)
    sch3 = scheduler.Scheduler(frame_rx_q3,ctrl_q3,data_q3,mgmt_q3)
    sch3.start()
    tr3 = transmitFrame.TransmitFrame(frame_tx_q3,tx_ev_q3)
    tr3.start()
    net_conf3 = NetworkConfiguration.NetworkConfiguration("103",'my network',"256",1)
    net_conf3.retry_timeout = 5    
    dpcontrol3 =  DiscoveryPeeringController.DiscoveryPeeringController(net_conf3,None,mgmt_q3,tx_ev_q3)
    dpcontrol3.start()
    myBeacon3 = Beacon.Beacon(net_conf3 ,tx_ev_q3)
    myBeacon3.start()    
    "---------------------FIN NODO 102 -----------------------------------------------"



    vc= virtualchannel.VirtualChannel(frame_tx_q2)
    vc.add(frame_rx_q1) 
    vc.add(frame_rx_q2)
    vc.add(frame_rx_q3)
    vc.start()




if __name__ == '__main__':
    try:
        simulates()
    except KeyboardInterrupt:
        pass
        