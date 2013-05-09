# -*- coding: utf-8 -*-
"""
Created on Tue May  7 12:42:54 2013

@author: belza
"""
import sys
sys.path +=['..']
import Queue,time
import libfsm.fsm as fsm
import libevents.events as events
import libtimer.timer as Timer
import NetworkConfiguration

class DiscoveryPeeringFSM() :
    """   The discovery and peering finite state machine.
    
          This class implements the  state machine for Discovery and Peering (IEEE  Std 802.11-2012  pg 1365).       
    """

    def __init__(self,link_id,network_conf,tx_event_q,event_q):
        '''  
        Constructor
        @param link_id: each state machine is associated with a network link. This is the identification of the link or the state machine.
        @param network_conf : actual network configuration.        
        @param tx_event_q : The event queue where to put the new events.
        @param event_q : The event queue of the fsm controller. Will be passed to the Timers in order to generates Timer events to the fsm controller
        
        '''
        self.tx_event_q = tx_event_q
        self.event_q = event_q
        self.net_conf = network_conf
        self.link_id = link_id
        self.timerRetry = None
        self.timerHolding =None
        self.timerConfirm =None

        self.fsm = fsm.FSM ('IDLE', []) # "memory" will be used as a stack.
        self.fsm.set_default_transition (self.Error, 'IDLE')
        self.fsm.add_transition_any  ('IDLE', None, 'IDLE')
        
        "------------------ Transitions from IDLE -----------------------------------------------------------"
        self.fsm.add_transition      ('REQ_RJCT',               'IDLE',            self.sndCLS,              'IDLE')
        self.fsm.add_transition      ('ACTOPN',                 'IDLE',            self.sndOPNsetR,          'OPN_SNT')
        self.fsm.add_transition      ('OPN_ACPT',               'IDLE',            self.sndCNFsetR,          'OPN_RCVD')
    
        "------------------ Transitions from OPN_SNT -----------------------------------------------------------"        
        self.fsm.add_transition      ('TOR1',                   'OPN_SNT',         self.sndOPNsetR,          'OPN_SNT')
        self.fsm.add_transition      ('CNF_ACPT',               'OPN_SNT',         self.clRsetC,             'CNF_RCVD')
        self.fsm.add_transition      ('OPN_ACPT',               'OPN_SNT',         self.sndCNF,              'OPN_RCVD')
        self.fsm.add_transition_list      (['CLS_ACPT', 'OPN_RJCT', 'CNF_RJCT', 'TOR2', 'CNCL'],   'OPN_SNT',      self.sndCLSclRsetH,   'HOLDING')
        
        "------------------ Transitions from CNF_RCVD -----------------------------------------------------------"      
        self.fsm.add_transition      ('OPN_ACPT',               'CNF_RCVD',         self.clCsndCNF,              'ESTAB')
        self.fsm.add_transition_list      (['CLS_ACPT', 'OPN_RJCT', 'CNF_RJCT', 'CNCL'],   'CNF_RCVD',     self.sndCLSclCsetH,   'HOLDING')
        self.fsm.add_transition      ('TOC',   'CNF_RCVD',    self.sndCLSsetH,   'HOLDING')
    
        "------------------ Transitions from OPN_RCVD -----------------------------------------------------------"      
        self.fsm.add_transition      ('OPN_ACPT',               'OPN_RCVD',         self.sndCNF,              'OPN_RCVD')
        self.fsm.add_transition      ('TOR1',                   'OPN_RCVD',         self.sndOPNsetR,          'OPN_RCVD')
        self.fsm.add_transition      ('CNF_ACPT',               'OPN_RCVD',         self.clR,                 'ESTAB')
        self.fsm.add_transition_list      (['CLS_ACPT', 'OPN_RJCT', 'CNF_RJCT', 'TOR2', 'CNCL'],   'OPN_RCVD',      self.sndCLSclRsetH,   'HOLDING')    
        
        "------------------ Transitions from ESTAB -----------------------------------------------------------"      
        self.fsm.add_transition      ('OPN_ACPT',               'ESTAB',         self.sndCNF,              'ESTAB')
        self.fsm.add_transition_list      (['CLS_ACPT', 'OPN_RJCT', 'CNF_RJCT', 'CNCL'],   'ESTAB',     self.sndCLSsetH,   'HOLDING')
    
        "------------------ Transitions from HOLDING -----------------------------------------------------------"      
        self.fsm.add_transition      ('TOH',               'HOLDING',         None,              'IDLE')
        self.fsm.add_transition      ('CLS_ACPT',          'HOLDING',         self.clH,               'IDLE')
        self.fsm.add_transition_list      (['OPN_ACPT','CNF_ACPT', 'OPN_RJCT', 'CNF_RJCT', 'CNCL'],   'HOLDING',     self.sndCLS,   'HOLDING')
        
    def appendToMemory(self,data):    
        self.fsm.memory.append (data) 
        
    def sndCLS(self,fsm):
        event = events.EventFrame("Mgmt","Close")
        self.tx_event_q.put(event,False)
    
    def sndOPN(self,fsm):
        event = events.EventFrame("Mgmt","Open")
        self.tx_event_q.put(event,False)

    def sndCNF(self,fsm):
        event = events.EventFrame("Mgmt","Confirm")
        self.tx_event_q.put(event,False)

    def setR(self,fsm):
        self.timerRetry=Timer.Timer(self.event_q,self.net_conf.retry_timeout,self.net_conf.max_retry,"TOR1", self.link_id,"TOR2" )
        self.timerRetry.start()
        
    def setC(self,fsm):
        self.timerConfirm=Timer.Timer(self.event_q,self.net_conf.confirm_timeout,1,"TOC", self.link_id )
        self.timerConfirm.start()
        
    def setH(self,fsm):
        self.timerHolding=Timer.Timer(self.event_q,self.net_conf.holding_timeout,1,"TOH", self.link_id )
        self.timerHolding.start()

    def clH(self,fsm):
       self.timerHolding.stop()
 
    def clR(self,fsm):
       self.timerRetry.stop()

    def clC(self,fsm):
       self.timerConfirm.stop()

    def sndOPNsetR(self,fsm):
        self.sndOPN(fsm)
        self.setR(fsm)

    def sndCNFsetR(self,fsm):
        self.sndCNF(fsm)
        self.setR(fsm)
        
    def clRsetC(self,fsm):
        self.clR(fsm)
        self.setC(fsm)
        
    def sndCLSclRsetH(self,fsm):
        self.sndCLS(fsm)
        self.clR(fsm)
        self.setH(fsm)

    def clCsndCNF(self,fsm):
        self.clC(fsm)
        self.sndCNF(fsm)
        
    def sndCLSclCsetH(self,fsm):
        self.sndCLS(fsm)
        self.clC(fsm)
        self.setH(fsm)
        
    def sndCLSsetH(self,fsm):
        self.sndCLS(fsm)
        self.setH(fsm)


    def Error (self,fsm):
        print 'That does not compute the state machine.'
        print str(fsm.input_symbol)



def test():
    tx_event_q=Queue.Queue(10)
    event_q=Queue.Queue(10)
    net_conf1 = NetworkConfiguration.NetworkConfiguration(100,'my network',256,1)
    mydpfsm = DiscoveryPeeringFSM(127, net_conf1,tx_event_q,event_q)
    mydpfsm.fsm.process("ACTOPN")    
    event=tx_event_q.get()        
    print " event transmited ", event.ev_subtype, " ", int(round(time.time() * 1000)) 
    print "Nuevo Estado: ", mydpfsm.fsm.current_state        
    event= event_q.get()
    print " event arrives at the fsm controller ", event.ev_subtype, " ",event.add_info, int(round(time.time() * 1000))    
 

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
