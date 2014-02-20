# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:55:46 2013

@author: belza
"""

import sys
sys.path +=['..']

import Queue
import libmanagement.NetworkConfiguration as NetworkConfiguration
import libmacTDMA.MacTdma as Mac
import libadaptationlayer.scheduler as scheduler
import libadaptationlayer.transmitFrame as transmitFrame
import virtualchannel
import libadaptationlayer.schedEvToFr as schedEvToFr
import libadaptationlayer.schedFrToEv as schedFrToEv
import libutils.gnlogger as gnlogger
import logging
import libvirtualchannel.EventConsumer as EventConsumer
import libvirtualchannel.EventSimulator as EventSimulator
module_logger = logging.getLogger(__name__)


def simulates():
    gnlogger.logconf()         # initializes the logging facility
    module_logger.info('start this module')
    "-------------------NODO 100 MASTER-------------------------------------------------------"    
   
    L1_ctrl_rx_q1 = Queue.Queue(10)
    L1_data_rx_q1 = Queue.Queue(10)
    L2_ctrl_rx_q1 = Queue.Queue(10)
    L2_data_rx_q1 = Queue.Queue(10)
    L1_event_tx_q1 = Queue.Queue(10)
    L2_event_tx_q1 = Queue.Queue(10)
    
    frame_rx_q1 = Queue.Queue(10)
    frame_tx_q1 = Queue.Queue(10)

    out_queues1 = { \
        'Ctrl': (L1_ctrl_rx_q1), \
        'Mgmt': (L1_ctrl_rx_q1), \
        'Data': (L1_data_rx_q1)  \
        }
    sch1 = schedFrToEv.SchedFrToEv(frame_rx_q1, out_queues1)
    sch1.start()
    
    # Configuration of the scheduler of Node 1 that receives events and generates frame events.
   
    out_queues_tx1 = { \
        'frames':    (frame_tx_q1) \
    }
    tx1 = schedEvToFr.SchedEvToFr( L1_event_tx_q1, out_queues_tx1)
    tx1.start()

                
    net_conf1 = NetworkConfiguration.NetworkConfiguration(100,'my network',256,1)
    net_conf1.slots = 3 
    " The first slot  is the control slot, the others are for data"
    net_conf1.control_time = 3
    " Each slot has 1 second"
    net_conf1.list_nodes.append(100)
    net_conf1.list_nodes.append(101)
    
    mac_control1 = Mac.MacTdma(net_conf1,L1_ctrl_rx_q1,L1_data_rx_q1,L2_ctrl_rx_q1,L2_data_rx_q1,L1_event_tx_q1,L2_event_tx_q1,True)

    mySimulator1 = EventSimulator.EventSimulator( 100,"DataData",L2_data_rx_q1 ,100,100)
    mySimulator1.start()


    myConsumer1 = EventConsumer.EventConsumer("N1--L3consumer",L2_event_tx_q1)
    myConsumer1.start()

    
    "---------------------FIN NODO 100 -----------------------------------------------"
#    
    
    "-------------------NODO 101 SLAVE-------------------------------------------------------"   
    
    L1_ctrl_rx_q2 = Queue.Queue(10)
    L1_data_rx_q2 = Queue.Queue(10)
    L2_ctrl_rx_q2 = Queue.Queue(10)
    L2_data_rx_q2 = Queue.Queue(10)
    L1_event_tx_q2 = Queue.Queue(10)
    L2_event_tx_q2 = Queue.Queue(10)
    
    frame_rx_q2 = Queue.Queue(10)
    frame_tx_q2 = frame_tx_q1

    out_queues2 = { \
        'Ctrl': (L1_ctrl_rx_q2), \
        'Mgmt': (L1_ctrl_rx_q2), \
        'Data': (L1_data_rx_q2)  \
        }
    sch2 = schedFrToEv.SchedFrToEv(frame_rx_q2, out_queues2)
    sch2.start()
    
    # Configuration of the scheduler of Node 1 that receives events and generates frame events.
   
    out_queues_tx2 = { \
        'frames':    (frame_tx_q2) \
    }
    tx2 = schedEvToFr.SchedEvToFr( L1_event_tx_q2, out_queues_tx2)
    tx2.start()

                
    net_conf2 = NetworkConfiguration.NetworkConfiguration(101,'my network',256,1)
    "Lo que sigue no es necesario porque solo se usa lo configurado en el MASTER" 
#    net_conf2.slots = 3 
#    " The first slot  is the control slot, the others are for data"
#    net_conf2.control_time = 3
#    " Each slot has 1 second"
#    net_conf2.list_nodes.append(100)
#    net_conf2.list_nodes.append(101)
    
    mac_control2 = Mac.MacTdma(net_conf2,L1_ctrl_rx_q2,L1_data_rx_q2,L2_ctrl_rx_q2,L2_data_rx_q2,L1_event_tx_q2,L2_event_tx_q2,False)

    mySimulator2 = EventSimulator.EventSimulator( 100,"DataData",L2_data_rx_q2 ,101,100)
    mySimulator2.start()


    myConsumer2 = EventConsumer.EventConsumer("N2 ---L3consumer",L2_event_tx_q2)
    myConsumer2.start()

    
    
    "---------------------FIN NODO 101 -----------------------------------------------"

 
    


    vc= virtualchannel.VirtualChannel(frame_tx_q2)
    vc.add(frame_rx_q1) 
    vc.add(frame_rx_q2)
    vc.start()




if __name__ == '__main__':
    try:
        simulates()
    except KeyboardInterrupt:
        pass
        