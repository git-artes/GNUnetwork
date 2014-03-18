# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:55:46 2013

@author: belza
"""

import sys
sys.path +=['..']

import Queue
import virtualchannel
import libadaptlay80211.schedEvToFr as schedEvToFr
import libadaptlay80211.schedFrToEv as schedFrToEv
import libutils.gnlogger as gnlogger
import logging
import libvirtualchannel.EventConsumer as EventConsumer
import libvirtualchannel.EventSimulator as EventSimulator
module_logger = logging.getLogger(__name__)


def simulates():
    gnlogger.logconf()         # initializes the logging facility
    module_logger.info('start this module')
    "-------------------NODO 100 MASTER-------------------------------------------------------"    
   
    L2_ctrl_rx_q1 = Queue.Queue(10)
    L2_data_rx_q1 = Queue.Queue(10)
    L2_mgmt_rx_q1 = Queue.Queue(10)
    L2_event_tx_q1 = Queue.Queue(10)
    
    frame_rx_q1 = Queue.Queue(10)
    frame_tx_q1 = Queue.Queue(10)

    out_queues1 = { \
        'Ctrl': (L2_ctrl_rx_q1), \
        'Mgmt': (L2_mgmt_rx_q1), \
        'Data': (L2_data_rx_q1)  \
        }
    sch1 = schedFrToEv.SchedFrToEv(frame_rx_q1, out_queues1)
    sch1.start()
    
    # Configuration of the scheduler of Node 1 that receives events and generates frame events.
   
    out_queues_tx1 = { \
        'frames':    (frame_tx_q1) \
    }
    tx1 = schedEvToFr.SchedEvToFr( L2_event_tx_q1, out_queues_tx1)
    tx1.start()

                
  

    mySimulator1 = EventSimulator.EventSimulator( 15,"CtrlRTS",L2_event_tx_q1 ,"100000","101000")
    mySimulator1.start()


    myConsumer1 = EventConsumer.EventConsumer("N1--L3consumer",L2_data_rx_q1)
    myConsumer1.start()

    
    "---------------------FIN NODO 100 -----------------------------------------------"
#    
    
    "-------------------NODO 101 -------------------------------------------------------"   
    
    L2_ctrl_rx_q2 = Queue.Queue(10)
    L2_data_rx_q2 = Queue.Queue(10)
    L2_mgmt_rx_q2 = Queue.Queue(10)
    L2_event_tx_q2 = Queue.Queue(10)
    
    frame_rx_q2 = Queue.Queue(10)
    frame_tx_q2 = frame_tx_q1

    out_queues2 = { \
        'Ctrl': (L2_ctrl_rx_q2), \
        'Mgmt': (L2_ctrl_rx_q2), \
        'Data': (L2_data_rx_q2)  \
        }
    sch2 = schedFrToEv.SchedFrToEv(frame_rx_q2, out_queues2)
    sch2.start()
    
    # Configuration of the scheduler of Node 1 that receives events and generates frame events.
   
    out_queues_tx2 = { \
        'frames':    (frame_tx_q2) \
    }
    tx2 = schedEvToFr.SchedEvToFr( L2_event_tx_q2, out_queues_tx2)
    tx2.start()

       

    mySimulator1 = EventSimulator.EventSimulator( 15,"CtrlCTS",L2_event_tx_q2 ,"101000","100000")
    mySimulator1.start()


    myConsumer1 = EventConsumer.EventConsumer("N1--L3consumer",L2_data_rx_q2)
    myConsumer1.start()         

    
    
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
        