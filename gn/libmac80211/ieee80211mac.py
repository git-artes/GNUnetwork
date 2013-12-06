# -*- coding: utf-8 -*-
"""
@author: ggomez
"""
import sys
sys.path +=['..']
import Queue,time,threading
import libfsm.fsm as fsm
import libevents.if_events as if_events
import libtimer.timer as Timer
import libmanagement.NetworkConfiguration as NetworkConfiguration
import libtimer.timer as Timer

aSIFSTime = 1
CTSTime = 4
aSlotTime = 2
aRTSThreshold = 20
dot11LongRetryLimit = 100

class ieee80211mac() :
    """   The 802.11 mac finite state machine.
	"""
	
    def __init__( self, tname, net_conf, timer_q, tx_ql1, tx_ql3 ):
		'''  
			Constructor
			@param tx_q: The transmition event queue ( Events to layer 1 )
        
		'''
		self.tx_ql1 = tx_ql1
		self.tx_ql3 = tx_ql3
		self.net_conf = net_conf
		self.tname = tname
		self.timer_q = timer_q
		self.tout = 100
		
		self.LRC = 0 # Long Retry Counter
		self.SRC = 0 # Short Retry Counter
		self.NAV = 0 # Network Allocation Vector
		self.PAV = 0 # Physical Allocation Vector
	
		log( self.tname, 'MAC: init' )
		self.mac_fsm = fsm.FSM ('IDLE', []) 
		self.mac_fsm.set_default_transition ( self.Error, 'IDLE')

		self.mac_fsm.add_transition      ('Data',		    'IDLE',            self.rcvL3,      'WAIT_ACK'	)
		self.mac_fsm.add_transition      ('Beacon',		    'IDLE',            self.rcvL3,      'WAIT_ACK'	)
		self.mac_fsm.add_transition      ('L2_DATA',		'IDLE',        	   self.rcvL2,      'IDLE'	 	)
		self.mac_fsm.add_transition      ('RTS',            'IDLE',        	   self.rcvRTS,     'IDLE'		)
		self.mac_fsm.add_transition      ('CTS',            'IDLE',        	   self.updNAV,     'IDLE'    	)
		self.mac_fsm.add_transition_any  (					'IDLE', 		   self.Error, 	   	'IDLE'    	)

		self.mac_fsm.add_transition      ('ACK',            'WAIT_ACK',        self.rcvACK, 	'IDLE'    	)
		self.mac_fsm.add_transition      ('Timer',          'WAIT_ACK',        self.sndData,    'WAIT_ACK'	)
		self.mac_fsm.add_transition      ('RTS',            'WAIT_ACK',        self.rcvRTS,     'WAIT_CTS'	)
		self.mac_fsm.add_transition_any  (					'WAIT_ACK', 	   self.Error, 	   	'WAIT_ACK'	)

		self.mac_fsm.add_transition      ('CTS',            'WAIT_CTS',        self.sndData,    'WAIT_ACK'	)
		self.mac_fsm.add_transition      ('Timer',          'WAIT_CTS',        self.sndRTS,     'WAIT_CTS'	)
		self.mac_fsm.add_transition      ('RTS',            'WAIT_CTS',        self.rcvRTS,     'WAIT_CTS'	)
		self.mac_fsm.add_transition_any  (					'WAIT_CTS', 	   self.Error, 	   	'WAIT_CTS'	)

    def Error ( self, fsm ):
		log( self.tname, 'MAC: Error: Default transition for symbol: '+ str( fsm.input_symbol ) + " state: " + str( fsm.current_state ) )
		return True

    def rcvL3( self, fsm ):
		log( self.tname, 'MAC: Receive from L3' )
		event = self.mac_fsm.memory
		if ( event.ev_dc['frame_length'] > aRTSThreshold ):
			self.sndRTS( fsm )
			self.start_timer()
			self.mac_fsm.next_state = 'WAIT_CTS'
		else:
			self.sndData( fsm )
			self.start_timer()
		return True

    def sndData ( self, fsm ):
		log( self.tname, 'MAC: Send Data' )
		self.snd_frame( self.mac_fsm.memory )
		return True

    def snd_frame( self, event ):
		log( self.tname, 'MAC: Send Frame' )
		if ( self.SRC == 0 and self.LRC == 0 ):
			if ( not self.freeChannel() ):
				self.waitfree()
				self.backoff()
		else:
			CW = min( CW*2+1, aCWmax ) 			## en el tutorial dice max() pero no puede ser
			if event.frame_length > aRTSThreshold:
				self.LRC += 1
				if ( self.LRC >= dot11LongRetryLimit ):
					self.discard()
					CW = aCWmin
					self.LRC = 0
					return
			else:
				self.SRC += 1
				if ( self.SRC >= dot11ShortRetryLimit ):
					self.discard()
					CW = aCWmin
					self.SRC = 0
					return
			self.backoff()
		self.sendtoL1( event )
		return True
		
    def sndRTS ( self, fsm ):
		log( self.tname, 'MAC: Send RTS' )
		event = if_events.mkevent("CtrlRTS")
		event.ev_dc['src_addr']=self.net_conf.station_id
		rcv_event = self.mac_fsm.memory
		event.ev_dc['dst_addr']= rcv_event.ev_dc['dst_addr']
		event.ev_dc['duration']=0;
		self.snd_frame( event )
		return True

    def sndCTS ( self, fsm ):
		log( self.tname, 'MAC: Send CTS' )
		event = if_events.mkevent("CtrlCTS")
		event.ev_dc['src_addr']=self.net_conf.station_id
		rcv_event = self.mac_fsm.memory
		event.ev_dc['dst_addr']= rcv_event.ev_dc['dst_addr']
		self.snd_frame( event )
		return True

    def rcvRTS ( self, fsm ):
		log( self.tname, 'MAC: Receive RTS' )
		self.updNAV( fsm )
		event = self.mac_fsm.memory
		if ( event.ev_dc['dst_addr'] == self.net_conf.station_id ):
			log( self.tname, 'MAC: Receive RTS (for me)' )
			self.sndCTS( fsm )
		else:
			log( self.tname, 'MAC: Receive RTS (not for me, ignoring)' )
			self.mac_fsm.next_state = self.mac_fsm.current_state
		return True

    def updNAV ( self, fsm ):
		log( self.tname, 'MAC: Update NAV' )
		event = self.mac_fsm.memory
		if ( fsm.input_symbol == "RTS" ):
			waitT = 2*aSIFSTime + CTSTime + 2*aSlotTime
			time.sleep( waitT )
			self.NAV = self.currentTime()
		else:
			testNAV = self.currentTime() + int(event.ev_dc['duration'])
			if ( testNAV > self.NAV ):
				self.NAV = testNAV
		return True

    def sndACK ( self, fsm ):
		log( self.tname, 'MAC: Send ACK' )
		event = if_events.mkevent("CtrlACK")
		event.ev_dc['src_addr']=self.net_conf.station_id
		rcv_event = self.mac_fsm.memory
		event.ev_dc['dst_addr']= rcv_event.ev_dc['dst_addr']
		self.snd_frame( event )
		return True

    def rcvACK ( self, fsm ):
		log( self.tname, 'MAC: Receive ACK' )
		event = self.mac_fsm.memory
		CW = aCWmin
		if event.frame_length > aRTSThreshold:
			self.LRC = 0
		else:
			self.SRC = 0
		## TODO fragmentation 
		return True

    def sendtoL1( self, event ):
		log( self.tname, 'MAC: transmito al fin!!' )
		self.tx_ql1.put( event, False )
		return True
				
    def backoff():
		log( self.tname, 'MAC: backoff' )
		if ( BC == 0 ):
			BC = random.randint( 0, CW )
		while ( BC != 0 ):
			time.sleep( TimeSlot )
			if ( max( self.NAV, self.PAV ) < ( self.currentTime() - TimeSlot ) ):
				BC -= 1
			else:
				while ( not self.freeChannel() ):
					self.waitfree()
				time.sleep( DIFS )
		return True

    def rcvL2 ( self, fsm ):
		log( self.tname, 'MAC: rcv L2' )
		self.updNAV( fsm )
		time.sleep( SIFS )
		self.sndACK( fsm )
		return True

    def currentTime( self ):
		log( self.tname, 'MAC: get Current Time' )
		return time.time()

    def freeChannel( self ):
		log( self.tname, 'MAC: freeChannel?' )
		return True

    def waitfree( self ):
		log( self.tname, 'MAC: waitfree' )
		time.sleep( 1 )
		return True

    def discard( self ):
		log( self.tname, 'MAC: discard' )
		return True

    def start_timer( self ):
		log( self.tname, 'MAC: start timer' )
		timer=Timer.Timer( self.timer_q, self.tout, 1, "TimerTimer" )
		timer.start()
		return True

def test():
    rx_q_l1 = Queue.Queue( 10 )
    rx_q_l3 = Queue.Queue( 10 )
    tx_q = Queue.Queue( 10 )
    net_conf = NetworkConfiguration.NetworkConfiguration(100,'my network',256,1)

    mymac = ieee80211mac( net_conf, tx_q )

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
    ev = events.mkevent("CtrlRTS")
    ev.ev_dc['src_addr']=100
    ev.ev.dc['dst_addr']=100
    mymac.mac_fsm.memory = ev
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
                        
class ControllerMAC(threading.Thread) :
 
    def __init__(self, net_conf, rxq_l1_ctrl, rxq_l1_mgmt, rxq_l1_data, txq_l1, rxq_l3, txq_l3 ):
        threading.Thread.__init__(self)
        self.net_conf = net_conf
        self.rx_q_l1c = rxq_l1_ctrl
        self.rx_q_l1m = rxq_l1_mgmt
        self.rx_q_l1d = rxq_l1_data
        self.rx_q_l3 = rxq_l3
        self.tx_q_l1 = txq_l1
        self.tx_q_l3 = txq_l3
        self.finished = False
        self.mymac = None        
        self.tname = self.net_conf.station_id
        self.timer_q = Queue.Queue( 10 )

    def run(self):
        self.mymac = ieee80211mac( self.tname, self.net_conf, self.timer_q, self.tx_q_l1, self.tx_q_l3 )
        while not self.finished:
			# read timer events
			if ( not self.timer_q.empty() ):
				event = self.timer_q.get_nowait()
				log( self.tname, "MAC: Timer event arrives at the fsm controller " )
				print event, " ", int(round(time.time() * 1000))
				log( self.tname, "MAC: state before processing event " + str( self.mymac.mac_fsm.current_state ) )
				self.mymac.mac_fsm.memory = event
				self.mymac.mac_fsm.process( event.ev_subtype )
				log( self.tname, "MAC: state after processing event " + str( self.mymac.mac_fsm.current_state ) )
			# read control frames from L1
			if ( not self.rx_q_l1c.empty() ):
				event = self.rx_q_l1c.get_nowait()
				log( self.tname, "MAC: L1 control event arrives at the fsm controller " )
				print event, " ", int(round(time.time() * 1000))
				log( self.tname, "MAC: state before processing event " + str( self.mymac.mac_fsm.current_state ) )
				self.mymac.mac_fsm.memory = event
				self.mymac.mac_fsm.process( event.ev_subtype )
				log( self.tname, "MAC: state after processing event " + str( self.mymac.mac_fsm.current_state ) )
			# read data frames from L1
			if ( not self.rx_q_l1d.empty() ):
				event = self.rx_q_l1d.get_nowait()
				log( self.tname, "MAC: L1 data event arrives at the fsm controller " )
				print event, " ", int(round(time.time() * 1000)) 
				log( self.tname, "MAC: state before processing event " + str( self.mymac.mac_fsm.current_state ) )
				self.mymac.mac_fsm.memory = event
				self.mymac.mac_fsm.process( event.ev_subtype )
				log( self.tname, "MAC: state after processing event " + str( self.mymac.mac_fsm.current_state ) )
			# read management frames from L1
			#if ( not self.rx_q_l1m.empty() ):
			#	event = self.rx_q_l1m.get_nowait()
			#	log( self.tname, "MAC: L1 management event arrives at the fsm controller ", event, " ", int(round(time.time() * 1000)) )
			#	log( self.tname, "MAC: state before processing event ", self.mac_fsm.current_state )
			#	self.mac_fsm.memory = event
			#	self.mac_fsm.process( event.ev_subtype )
			#	log( self.tname, "MAC: state after processing event ", self.mac_fsm.current_state )
			# read from L3
			if ( not self.rx_q_l3.empty() ):
				event = self.rx_q_l3.get_nowait()
				log( self.tname, "MAC: L3 event arrives at the fsm controller " )
				print event, " ", int(round(time.time() * 1000)) 
				log( self.tname, "MAC: state before processing event " + str( self.mymac.mac_fsm.current_state) )
				self.mymac.mac_fsm.memory = event
				self.mymac.mac_fsm.process( event.ev_subtype )
				log( self.tname, "MAC: state after processing event " + str( self.mymac.mac_fsm.current_state ) )
			
    def stop(self):
        print "MAC: STOP Controller fsm emulator CALLED"
        self.finished = True
        print "MAC: Controller DONE"
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
			print "MAC: L2 event arrives at the fsm controller ", event, " ", int(round(time.time() * 1000)) 
			print "MAC: state before processing event ", self.mac_fsm.current_state 
			self.mac_fsm.memory = event
			self.mac_fsm.process( event.ev_subtype )
			print "MAC: state after processing event ", self.mac_fsm.current_state
			# read from L3
			event = self.rx_q_l3.get_nowait()
			print "MAC: L3 event arrives at the fsm controller ", event, " ", int(round(time.time() * 1000)) 
			print "MAC: state before processing event ", self.mac_fsm.current_state 
			self.mac_fsm.memory = event
			self.mac_fsm.process( event.ev_subtype )
			print "MAC: state after processing event ", self.mac_fsm.current_state
			
    def stop(self):
        print "MAC: STOP Controller fsm emulator CALLED"
        self.finished = True
        print "MAC: Controller DONE"
        self._Thread__stop()
        
def log( tname, msg ):
    print "\n" + tname + " " + msg
    
if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
