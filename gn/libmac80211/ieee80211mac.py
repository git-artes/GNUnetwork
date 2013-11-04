# -*- coding: utf-8 -*-
"""
@author: ggomez
"""
import sys
sys.path +=['..']
import Queue,time,threading
import libfsm.fsm as fsm
import libevents.events as events
import libtimer.timer as Timer

class ieee80211mac() :
	"""   The 802.11 mac finite state machine.
    
	"""
	
	def __init__( self, tx_q ) :
		'''  
			Constructor
			@param tx_q: The transmition event queue ( Events to layer 1 )
        
		'''
		self.tx_q = tx_q
	
		print 'MAC: init'
		self.mac_fsm = fsm.FSM ('IDLE', []) 
		self.mac_fsm.set_default_transition ( self.Error, 'IDLE')

		self.mac_fsm.add_transition      ('L3_DATA',		'IDLE',            self.rcvL3,      'WAIT_ACK'	)
		self.mac_fsm.add_transition      ('L2_DATA',		'IDLE',        	   self.rcvL2,      'IDLE'	 	)
		self.mac_fsm.add_transition      ('RTS',            'IDLE',        	   self.rcvRTS,     'WAIT_CTS'	)
		self.mac_fsm.add_transition      ('CTS',            'IDLE',        	   self.updNAV,     'IDLE'    	)
		self.mac_fsm.add_transition_any  (					'IDLE', 		   self.Error, 	   	'IDLE'    	)

		self.mac_fsm.add_transition      ('ACK',            'WAIT_ACK',        self.rcvACK, 	'IDLE'    	)
		self.mac_fsm.add_transition      ('TIMER',          'WAIT_ACK',        self.sndData,    'WAIT_ACK'	)
		self.mac_fsm.add_transition_any  (					'WAIT_ACK', 	   self.Error, 	   	'WAIT_ACK'	)

		self.mac_fsm.add_transition      ('RTSSent',        'WAIT_ACK',        None,       		'WAIT_CTS'	)

		self.mac_fsm.add_transition      ('CTS',            'WAIT_CTS',        self.sndData,    'WAIT_ACK'	)
		self.mac_fsm.add_transition      ('TIMER',          'WAIT_CTS',        self.sndRTS,     'WAIT_CTS'	)
		self.mac_fsm.add_transition_any  (					'WAIT_CTS', 	   self.Error, 	   	'WAIT_CTS'	)

	def Error ( self, fsm ):
		print 'Error: Default transition for symbol: '
		print str( fsm.input_symbol )

	def rcvL3( self, fsm ):
		if ( frame_length > aRTSThreshold ):
			snd_frame( RTS )
			start_timer()
			mac_fsm.process( RTSSent )
		else:
			snd_frame( DATA )
			start_timer()

	def sndData ( self, fsm ):
		snd_frame( DATA )

	def snd_frame( self, event ):
		print 'Retry Data'
		if ( SRC == 0 and LRC == 0 ):
			if ( not freeChannel() ):
				waitfree()
				backoff()
		else:
			CW = min( CW*2+1, aCWmax ) 			## en el tutorial dice max() pero no puede ser
			if frame_length > aRTSThreshold:
				LRC += 1
				if ( LRC >= dot11LongRetryLimit ):
					discard()
					CW = aCWmin
					LRC = 0
					return
			else:
				SRC += 1
				if ( SRC >= dot11ShortRetryLimit ):
					discard()
					CW = aCWmin
					SRC = 0
					return
			backoff()
		sendtoL1( event )
		start_timer()
		
 	def sndRTS ( self, fsm ):
		event = events.mkevent("CtrlRTS")
		event.src_addr=self.net_conf.station_id
		#event.dst_addr= self.peer_addr
		event.duration=0;
		snd_frame( event )

 	def sndCTS ( self, fsm ):
		event = events.mkevent("CtrlCTS")
		event.src_addr=self.net_conf.station_id
		#event.dst_addr= self.peer_addr
		snd_frame( event )

 	def rcvRTS ( self, fsm ):
		self.updNAV( fsm )
		if ( toMe() ):
			sndCTS( fsm );
			start_timer()

 	def updNAV ( self, fsm ):
		print 'Update NAV'
		if ( pkt.type == RTS ):
			waitT = 2*aSIFSTime + CTSTime + 2*aSlotTime
			time.sleep( waitT )
			NAV = currentTime()
		else:
			testNAV = currentTime() + pkt.duration 
			if ( testNAV > NAV ):
				NAV = testNAV

 	def rcvACK ( self, fsm ):
		print 'Receive ACK'
		CW = aCWmin
		if frame_length > aRTSThreshold:
			LRC = 0
		else:
			SRC = 0
		## TODO fragmentation 

	def sendtoL1( self, event ):
		print "transmito al fin!!"
		self.tx_q.put( event, False )
				
	def backoff():
		if ( BC == 0 ):
			BC = random.randint( 0, CW )
		while ( BC != 0 ):
			time.sleep( TimeSlot )
			if ( max( NAV, PAV ) < ( currentTime() - TimeSlot ) ):
				BC -= 1
			else:
				while ( not freeChannel() ):
					waitfree()
				time.sleep( DIFS )

 	def rcvL2 ( self, fsm ):
		print 'Send ACK'
		self.updNAV( fsm )
		time.sleep( SIFS )
		snd_frame( ACK )

	def currentTime():
		print "get Current Time"	


def test():
    rx_q_l1 = Queue.Queue( 10 )
    rx_q_l3 = Queue.Queue( 10 )
    tx_q = Queue.Queue( 10 )

    mymac = ieee80211mac( tx_q )

    read_tx = ReadQueueMACTxEmulator( tx_q )
    read_tx.start()

    read_rx = ControllerMACFsmEmulator( rx_q_l1, rx_q_l3, mymac.mac_fsm )
    read_rx.start() 
    
    "TEST 1: ON IDLE RECEIVE .... AND .... "
    print ""
    print "MAC START TEST 1 --------------------------------------------" 
    print "MAC STATE BEFORE PROCESS ..... ", mymac.mac_fsm.current_state
    mymac.mac_fsm.process('FRUIT')    
    print "MAC STATE AFTER PROCESS ...... ", mymac.mac_fsm.current_state
    print ""    
    "---------------------------------------------------------------------------------------"

    "TEST 1: ON IDLE RECEIVE .... AND .... "
    print ""
    print "MAC START TEST 1 --------------------------------------------" 
    print "MAC STATE BEFORE PROCESS ..... ", mymac.mac_fsm.current_state
    mymac.mac_fsm.process('RTS')    
    print "MAC STATE AFTER PROCESS ...... ", mymac.mac_fsm.current_state
    print ""    
    "---------------------------------------------------------------------------------------"

    if read_tx.isAlive():        
        read_tx.stop()
    if read_rx.isAlive():
        read_rx.stop()
    print "MAC FIN"       

        
class ReadQueueMACTxEmulator(threading.Thread) :
 
    def __init__(self,tx_q):
        threading.Thread.__init__(self)
        self.tx_q = tx_q
        self.finished = False
        
    def run(self):
        while not self.finished:
            event= self.tx_q.get()        
            print "MAC: event transmited ", event, " ", int(round(time.time() * 1000)) 
            
    def stop(self):
        print "MAC: STOP Tx Emulator CALLED"
        self.finished = True
        print "MAC: TX DONE"
        self._Thread__stop()
                        
class ControllerMACFsmEmulator(threading.Thread) :
 
    def __init__(self,event_q_l1, event_q_l3,fsm):
        threading.Thread.__init__(self)
        self.rx_q_l1 = event_q_l1
        self.rx_q_l3 = event_q_l3
        self.mac_fsm = fsm
        self.finished = False
    
    def run(self):
        while not self.finished:
			# read from L1
			event = self.rx_q_l1.get_nowait()
			print "MAC: L2 event arrives at the fsm controller ", event, " ",event.add_info, int(round(time.time() * 1000)) 
			print "MAC: state before processing event ", self.mac_fsm.current_state 
			self.mac_fsm.memory = event
			self.mac_fsm.process( event.ev_subtype )
			print "MAC: state after processing event ", self.mac_fsm.current_state
			# read from L3
			event = self.rx_q_l3.get_nowait()
			print "MAC: L3 event arrives at the fsm controller ", event, " ",event.add_info, int(round(time.time() * 1000)) 
			print "MAC: state before processing event ", self.mac_fsm.current_state 
			self.mac_fsm.memory = event
			self.mac_fsm.process( event.ev_subtype )
			print "MAC: state after processing event ", self.mac_fsm.current_state
			
    def stop(self):
        print "MAC: STOP Controller fsm emulator CALLED"
        self.finished = True
        print "MAC: Controller DONE"
        self._Thread__stop()
            
if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
