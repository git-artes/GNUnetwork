# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 14:55:52 2012

@author: belza
"""

import sys
sys.path +=['..']

import threading
import PeersTable


class DiscoveryPeeringController(threading.Thread) :
    """   The discovery and peering controller, it is a Thread.   
          This class control the entries of the peers table and the set of the state machines. Each peer link has associated one state machine,       
    """

    def __init__(self,network_conf,net_profile,q_event,tx_event_q):
        '''  
        Constructor
        
        @param network_conf : actual network configuration.        
        @param  net_profile: network profile.        
        @param q_event : The event queue where this object gets the events to be precessed.        
        @param tx_event_q : The event queue where to put the new events.
        
        '''
        threading.Thread.__init__(self)
        self.my_addr = network_conf. getStationId()
        self.broadcast_addr =network_conf.getBroadcastAddr()
        self.my_profile = net_profile
        self.my_peers = PeersTable.PeersTable()
        " Each peer link has an identifier local_linkId. It is assigned when the peer link is created. It is inicialized when the class is created."
        self.local_linkId=0          
        self.net_conf = network_conf 
        self.my_queue = q_event
        self.tx_event_q =tx_event_q
        self.finished = False
      
   
    def run(self):
        while not self.finished :
            event= self.my_queue.get()
            if event.ev_type == "Timer":
                sm= self.my_peers.getSM(localLinkId = event.add_info )
                sm.fsm.process(event.ev_subtype) 
            else:
                if event.ev_type == "Mgmt":        
                    if (event.dst_addr == self.my_addr or event.dst_addr == self.broadcast_addr) and event.src_addr() != self.my_addr :
                        "In this case the destination mac is my mac or is a broadcast packet and I am not the source" 
                        if self.my_peers.isMember(peerMACaddr = event.src_addr):
                            "In this case the peer link exists in the peers table"
                            print "Evento 1: ", event,'  my mac: ',self.my_addr, '\n'
                            self.my_peers.printPeersTable()                
                            sm= self.my_peers.getSM(peerMACadr= event.src_addr)
                            self.my_peers.updatePeerLinkId(event.src_addr, event.peerlinkId)
                            self.moveFSM(event,sm)
                            self.my_peers.printPeersTable()
                        else:
                            " In this case the peer link does not exist in the peer table "
                            print "Evento 2: ", event,'  my mac: ',self.my_addr,'\n'
                            self.my_peers.printPeersTable()
                            self.local_linkId = self.local_linkId +1
                            self.my_peers.add(self,event.src_addr, self.my_queue, self.tx_event_q,self.net_conf,self.local_linkId,event.peerlinkId)
                            self.net_conf.number_of_peering = self.net_conf.number_of_peering+1                
                            sm= self.my_peers.getSM(peerMACaddr = event.src_addr)
                            self.moveFSM(event,sm)
                            print "Evento 3: ", event,'  my mac: ',self.my_addr,'\n'
                            self.my_peers.printPeersTable()
                    else:
                        print "Error: wrong MAC address, destination address:",  event.dst_addr, " source address : ", event.src_addr               
    
                else: 
                    print "Error: wrong event type"
                    
    def moveFSM(self,event,sm):
        if event.ev_nickname == "MgmtBeacon" and self.net_conf.accepting_additional_peerings :
            sm.fsm.process("ACTOPN")
        if event.ev_subtype == "ActionConfirm":                            
            sm.fsm.process("CONF_ACPT")
        if event.ev_subtype == "ActionClose":
            sm.fsm.process("CLS_ACPT")
        if event.ev_subtype == "ActionOpen" :
            if self.net_conf.accepting_additional_peerings:
                sm.fsm.process("OPN_ACPT")
            else:
                sm.fsm.process("OPN_RJCT")                                    

    def stop(self):
            self.finished = True
            self._Thread__stop()




def test():
    pass
    
if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
