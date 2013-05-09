# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 14:40:05 2012

@author: belza
"""
import SMDiscoveryPeering
from operator import itemgetter

class PeersTable :
    
    """ This class maintain the active peer links list.
        Each item of the list has the following elements: the peer MAC address, the local link Id, the peer Link Id and the corresponding state machine (object) of the PMP protocol.
        
    """
    def __init__(self):
        '''  
        Constructor: build an empty list    
        '''
        self.my_list=[]
  
        
    def add(self,my_controller,tx_frame_q,peerMACaddr,localLinkId,my_profile,peerLinkId=0):
        """
            Create the a state machine (SMDiscoveryPeering) and a new item to the peers list.
              
            @param my_controller: an object of the class DiscoveryPeeringController, it is necessary as areference for the state machine.        
        
            @param tx_frame_q:  the events transmition queue, it is necessary as a reference for the state machine.

            @param peerMACAddr:  The MAC address of the peer.

            @param localLinkId:  My link Id.

            @param my_profile:  The network Profile, it is necessary as a reference for the state machine.
            
            @param peerLinkId=0:  The link Id of my peer.

        
        """
        sm = SMDiscoveryPeering.SMDiscoveryPeering(my_profile,my_controller,tx_frame_q,peerMACaddr) 
        self.my_list.append({'peerMac':peerMACaddr,'localLinkId': localLinkId, 'peerLinkId': peerLinkId,'state_machine':sm})

    def getIndex(self,peerMACaddr):
        """ Given the peer MAC Address return the index in the list of peers.
        """
        return map(itemgetter('peerMac'), self.my_list).index(peerMACaddr)
        
    def delete(self,peerMACaddr):
        """ Delete the register of the peers list of the given MAC address.
        """
        if self.isMember(peerMACaddr):
            self.my_list.__delitem__(self.getIndex(peerMACaddr))

    def updatePeerLinkId(self,peerMACaddr, peerLinkId):
        """ if there exsits a register in the peers list for the given MAC address update the peer link Id element.
        
        """
        if self.isMember(peerMACaddr):
            self.my_list[self.getIndex(peerMACaddr)]['peerLinkId']=peerLinkId

    def isMember(self,peerMACaddr):
        return map(itemgetter('peerMac'), self.my_list).__contains__(peerMACaddr)

    def getSM(self,peerMACaddr):
        """ if there exsits a register in the peers list for the given MAC address gives the corresponding state machine object.
        
        """
        if self.isMember(peerMACaddr):        
            return  self.my_list[self.getIndex(peerMACaddr)]['state_machine']

    def getLocalLinkId(self,peerMACaddr):
        if self.isMember(peerMACaddr):        
            return  self.my_list[self.getIndex(peerMACaddr)]['localLinkId']

    def printPeersTable(self):
        """ Print the peers table. """
        print " PEERS TABLE: \n peerMAC,local link Id, Peer link Id, state \n"
        for i in range(0,len(self.my_list)):
            print "Register number :", i, '\n'
            print self.my_list[i]['peerMac'],  self.my_list[i]['localLinkId'], self.my_list[i]['peerLinkId'],self.my_list[i]['state_machine'].state, '\n'      


def test():
    p=PeersTable()
    p.add(255, 1)
    p.printPeersTable()
    
    
if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
