# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 14:55:52 2012

@author: belza
"""

import sys
sys.path +=['..']

import threading
import PeersTable
import libtimer.timer as Timer 


class DiscoveryPeeringController(threading.Thread) :
    """   The discovery and peering controller, it is a Thread.
    
          This class control the entries of the peers table and the state machine asociated with each entry.       
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
        self.local_linkId=0   
        self.my_actual_net_conf = network_conf 

        self.my_queue = q_event
        self.tx_event_q =tx_event_q
      
    def delete(self,event):
        addr= event.getPeerAddr()
        self.my_peers.delete(addr)
        self.my_actual_net_conf.number_of_peering = self.my_actual_net_conf.number_of_peering - 1                

    def run(self):
        while 1 :
            event= self.my_queue.get()                    
            if (event.getDstAddr() == self.my_addr or event.getDstAddr() == self.broadcast_addr) and event.getPeerAddr() != self.my_addr :
                if self.my_peers.isMember(event.getPeerAddr()):
                    print "Evento 1: ", event.sub_type,'  my mac: ',self.my_addr, '\n'
                    self.my_peers.printPeersTable()                
                    sm= self.my_peers.getSM(event.getPeerAddr())
                    self.my_peers.updatePeerLinkId(event.getPeerAddr(), event.getPeerLinkId())
                    sm.receiveEvent(event)
                    self.my_peers.printPeersTable()
                else:
                    print "Evento 2: ", event.sub_type,'  my mac: ',self.my_addr,'\n'
                    self.my_peers.printPeersTable()
                    self.local_linkId = self.local_linkId +1
                    self.my_peers.add(self,self.tx_event_q,event.getPeerAddr(),self.local_linkId,self.my_profile,event.getPeerLinkId())
                    self.my_actual_net_conf.number_of_peering = self.my_actual_net_conf.number_of_peering+1                
                    sm= self.my_peers.getSM(event.getPeerAddr())
                    sm.receiveEvent(event)
                    print "Evento 3: ", event.sub_type,'  my mac: ',self.my_addr,'\n'
                    self.my_peers.printPeersTable()
            else:
                print "Bad address"                
    
    def raiseHoldingTimer(self,sm):
        timer=Timer.Timer( self.my_queue, self.my_actual_net_conf.holding_timeout,1,self.my_addr,sm.my_peer_addr ,"TOH")
        timer.start()
    
    def raiseConfirmTimer(self,sm):
            timer=Timer.Timer( self.my_queue,self.my_actual_net_conf.confirm_timeout,1,self.my_addr,sm.my_peer_addr ,"TOC")
            timer.start()
            
    def raiseRetryTimer(self,sm):
            timer=Timer.Timer(self.my_queue,self.my_actual_net_conf.retry_timeout,self.my_actual_net_conf.max_retry,self.my_addr,sm.my_peer_addr, "TOR1","TOR2" )
            timer.start()
            


def test():
    pass
    
if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
