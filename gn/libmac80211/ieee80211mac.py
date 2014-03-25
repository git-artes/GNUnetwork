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
import random

Loses = 10
aSIFSTime = 1
aDIFSTime = 1
# "CTS_Time” shall be calculated using the length of the CTS frame and the data rate at which the RTS frame used for the most recent NAV update was received.
CTS_Time = 14/34000  # 14 bytes, 34M ??
aSlotTime = 1
aRTSThreshold = 60
aPHY_RX_START_Delay = 10
dot11LongRetryLimit = 5
dot11ShortRetryLimit = 5
CWmin = 15
CWmax = 1023
CTSTout = aSIFSTime + aSlotTime + aPHY_RX_START_Delay
ACKTout = aSIFSTime + aSlotTime + aPHY_RX_START_Delay

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
		
		self.LRC = 0 # Long Retry Counter
		self.SRC = 0 # Short Retry Counter
		self.NAV = 0 # Network Allocation Vector
		self.PAV = 0 # Physical Allocation Vector
		self.BC = 0 # Backoff
		self.CW = CWmin # Current Window

		self.datatosend = 0
	
		log( self.tname, 'MAC: init' )
		self.mac_fsm = fsm.FSM ('IDLE', []) 
		self.mac_fsm.set_default_transition ( self.Error, 'IDLE')

		self.mac_fsm.add_transition      ('L3Data',		    'IDLE',            self.rcvL3,      'WAIT_ACK'	)
		self.mac_fsm.add_transition      ('Beacon',		    'IDLE',            self.rcvL3,      'WAIT_ACK'	)
		self.mac_fsm.add_transition      ('L1Data',			'IDLE',        	   self.rcvL1,      'IDLE'	 	)
		self.mac_fsm.add_transition      ('RTS',            'IDLE',        	   self.rcvRTS,     'IDLE'		)
		self.mac_fsm.add_transition      ('CTS',            'IDLE',        	   self.updNAV,     'IDLE'    	)
		self.mac_fsm.add_transition_any  (					'IDLE', 		   self.Error, 	   	'IDLE'    	)

		self.mac_fsm.add_transition      ('ACK',            'WAIT_ACK',        self.rcvACK, 	'IDLE'    	)
		self.mac_fsm.add_transition      ('ACKTout',     	'WAIT_ACK',        self.sndData,    'WAIT_ACK'	)
		self.mac_fsm.add_transition      ('DataAbort',     	'WAIT_ACK',        self.sndData,    'WAIT_ACK'	)
		self.mac_fsm.add_transition      ('RTS',            'WAIT_ACK',        self.rcvRTS,     'WAIT_CTS'	)
		self.mac_fsm.add_transition_any  (					'WAIT_ACK', 	   self.Error, 	   	'WAIT_ACK'	)

		self.mac_fsm.add_transition      ('CTS',            'WAIT_CTS',        self.sndData,    'WAIT_ACK'	)
		self.mac_fsm.add_transition      ('CTSTout', 	    'WAIT_CTS',        self.sndRTS,     'WAIT_CTS'	)
		self.mac_fsm.add_transition      ('RTSAbort', 	    'WAIT_CTS',        self.sndRTS,     'WAIT_CTS'	)
		self.mac_fsm.add_transition      ('RTS',            'WAIT_CTS',        self.rcvRTS,     'WAIT_CTS'	)
		self.mac_fsm.add_transition_any  (					'WAIT_CTS', 	   self.Error, 	   	'WAIT_CTS'	)

    def Error ( self, fsm ):
		log( self.tname, 'MAC: Error: Default transition for symbol: '+ str( fsm.input_symbol ) + ", state: " + str( fsm.current_state ) )
		return True

    def rcvL3( self, fsm ):
		log( self.tname, 'MAC: Receive from L3' )
		event = self.mac_fsm.memory
		self.datatosend = self.mac_fsm.memory
		if ( event.ev_dc['frame_length'] > aRTSThreshold ):
			self.sndRTS( fsm )
			log( self.tname, 'MAC: start timer' )
			self.rtstimer=Timer.Timer( self.timer_q, CTSTout, dot11ShortRetryLimit, 'TimerCTSTout', 'TimerRTSAbort' )
			self.rtstimer.start()
			self.mac_fsm.next_state = 'WAIT_CTS'
		else:
			self.sndData( fsm )
			if ( self.datatosend.ev_dc['frame_length'] > aRTSThreshold ):
				self.datatimer=Timer.Timer( self.timer_q, ACKTout, dot11ShortRetryLimit, 'TimerACKTout', 'TimerDataAbort' )
			else:
				self.datatimer=Timer.Timer( self.timer_q, ACKTout, dot11LongRetryLimit, 'TimerACKTout', 'TimerDataAbort' )
			log( self.tname, 'MAC: start timer' )
			self.datatimer.start()
		return True

    def sndData ( self, fsm ):
		event = self.mac_fsm.memory
		if ( event.ev_subtype == 'ACKTout' ):
			if ( event.nickname == 'TimerDataAbort' ):
				log( self.tname, 'MAC: Send Data EXAUSTED' )
				self.datatimer.stop()
				return False
			elif ( event.nickname == 'TimerACKTout' ):
				log( self.tname, 'MAC: Send Data. Retry' )
				self.snd_frame( self.datatosend )
		else:
			##self.snd_frame( self.mac_fsm.memory )
			self.snd_frame( self.datatosend )
		return True

    def snd_frame( self, event ):
		log( self.tname, 'MAC: Send Frame' )
		txok = False;
		while ( txok == False ):
			log( self.tname, 'MAC: loop LRC: ' + str(self.LRC) + ', SRC: ' + str( self.SRC) )
			#if ( self.SRC == 0 and self.LRC == 0 ):		# 1er intento
			#	self.backoff()
			if ( not ( event.ev_dc['frame_length'] > aRTSThreshold and self.LRC == 0 ) and not ( event.ev_dc['frame_length'] <= aRTSThreshold and self.SRC == 0 ) ):
#				# self.backoff()
#			else:
				self.CW = min( self.CW*2+1, CWmax )
				log( self.tname, 'MAC: Send Frame new CW ' + str( self.CW ) )
				self.backoff()
			if ( self.freeChannel() ):
				self.sendtoL1( event )
				log( self.tname, 'MAC: Send Frame (done)' )
				txok = True
				break;
			if ( event.ev_dc['frame_length'] > aRTSThreshold ):
				self.LRC += 1
				if ( self.LRC >= dot11LongRetryLimit ):
					self.discard()
					self.CW = CWmin
					self.LRC = 0
					log( self.tname, 'MAC: LRC > ' + str( dot11LongRetryLimit ) )
					return False
			else:
				self.SRC += 1
				if ( self.SRC >= dot11ShortRetryLimit ):
					self.discard()
					self.CW = CWmin
					self.SRC = 0
					log( self.tname, 'MAC: SRC > ' + str( dot11ShortRetryLimit ) )
					return False
			self.backoff()
			log( self.tname, "MAC: Send Frame: keep waiting" )
		log( self.tname, 'MAC: Send Frame (done)' )
		return True
		
    def sndRTS ( self, fsm ):
		log( self.tname, 'MAC: Send RTS' )
		rcv_event = self.mac_fsm.memory
		event = if_events.mkevent("CtrlRTS")
		event.ev_dc['src_addr']=self.net_conf.station_id
		event.ev_dc['dst_addr']= rcv_event.ev_dc['dst_addr']
		event.ev_dc['duration']=0;
		self.snd_frame( event )
		return True

    def sndCTS ( self, fsm ):
		log( self.tname, 'MAC: Send CTS' )
		event = if_events.mkevent("CtrlCTS")
		event.ev_dc['src_addr']=self.net_conf.station_id
		rcv_event = self.mac_fsm.memory
		event.ev_dc['dst_addr']= rcv_event.ev_dc['src_addr']
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
			#waitT = 2*aSIFSTime + CTS_Time + 2*aSlotTime # tutorial
			waitT = 2*aSIFSTime + CTS_Time + aPHY_RX_START_Delay + 2*aSlotTime # norma
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
		event.ev_dc['dst_addr']= rcv_event.ev_dc['src_addr']
		# self.snd_frame( event )
		return True

    def rcvACK ( self, fsm ):
		log( self.tname, 'MAC: Receive ACK' )
		event = self.mac_fsm.memory
		if ( event.ev_dc['dst_addr'] == self.net_conf.station_id ):
			log( self.tname, 'MAC: Receive ACK (for me)' )
			self.CW = CWmin
			if ( event.ev_dc['frame_length'] > aRTSThreshold ):
				self.LRC = 0
			else:
				self.SRC = 0
			self.datatimer.stop()
			## TODO fragmentation 
		else:
			log( self.tname, 'MAC: Receive ACK (not for me, ignoring)' )
			self.mac_fsm.next_state = self.mac_fsm.current_state
		return True

    def sendtoL1( self, event ):
		log( self.tname, 'MAC: transmito al fin!!' )
		self.tx_ql1.put( event, False )
		return True
				
    def backoff( self ):
		log( self.tname, 'MAC: backoff BC: ' + str(self.BC) + ' CW: ' + str(self.CW) )
		if ( self.BC == 0 ):
			self.BC = random.randint( 0, self.CW )
			log( self.tname, 'MAC: backoff new BC: ' + str(self.BC) )
		while ( self.BC != 0 ):
			time.sleep( aSlotTime )
			if ( max( self.NAV, self.PAV ) < ( self.currentTime() - aSlotTime ) ):
				while ( not self.freeChannel() ):
					self.waitfree()
				self.BC -= 1
				log( self.tname, 'MAC: backoff new BC decrement: ' + str(self.BC) )
			else:
				while ( not self.freeChannel() ):
					self.waitfree()
				log( self.tname, 'MAC: backoff sleep aDIFSTime' )
				time.sleep( aDIFSTime )
		return True

    def rcvL1 ( self, fsm ):
		log( self.tname, 'MAC: rcv L1' )
		self.updNAV( fsm )
		event = self.mac_fsm.memory
		if ( event.ev_dc['dst_addr'] == self.net_conf.station_id ):
			log( self.tname, 'MAC: Receive L1 data (for me)' )
			self.tx_ql3.put( event, False )
			time.sleep( aSIFSTime )
			self.sndACK( fsm )
		else:
			log( self.tname, 'MAC: Receive L1 data (not for me, ignoring)' )
			self.mac_fsm.next_state = self.mac_fsm.current_state
		return True

    def currentTime( self ):
		log( self.tname, 'MAC: get Current Time' )
		return time.time()

    def freeChannel( self ):
		#log( self.tname, 'MAC: freeChannel?' )
		test = random.randint(0,100);
		if ( test > Loses ):
			log( self.tname, 'MAC: freeChannel: FREE' )
			return True
		else:
			log( self.tname, 'MAC: freeChannel: BUSY' )
			return False

    def waitfree( self ):
		log( self.tname, 'MAC: waitfree' )
		while ( not self.freeChannel() ):
			time.sleep( 1 )
		log( self.tname, 'MAC: waitfree, now free' )
		return True

    def discard( self ):
		log( self.tname, 'MAC: discard' )
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
				# print event, " ", int(round(time.time() * 1000))
				#log( self.tname, "MAC: state before processing event " + str( self.mymac.mac_fsm.current_state ) )
				self.mymac.mac_fsm.memory = event
				self.mymac.mac_fsm.process( event.ev_subtype )
				#log( self.tname, "MAC: state after processing event " + str( self.mymac.mac_fsm.current_state ) )
			# read control frames from L1
			if ( not self.rx_q_l1c.empty() ):
				event = self.rx_q_l1c.get_nowait()
				log( self.tname, "MAC: L1 control event arrives at the fsm controller " )
				# print event, " ", int(round(time.time() * 1000))
				#log( self.tname, "MAC: state before processing event " + str( self.mymac.mac_fsm.current_state ) )
				self.mymac.mac_fsm.memory = event
				self.mymac.mac_fsm.process( event.ev_subtype )
				#log( self.tname, "MAC: state after processing event " + str( self.mymac.mac_fsm.current_state ) )
			# read data frames from L1
			if ( not self.rx_q_l1d.empty() ):
				event = self.rx_q_l1d.get_nowait()
				log( self.tname, "MAC: L1 data event arrives at the fsm controller " )
				# print event, " ", int(round(time.time() * 1000)) 
				#log( self.tname, "MAC: state before processing event " + str( self.mymac.mac_fsm.current_state ) )
				self.mymac.mac_fsm.memory = event
				self.mymac.mac_fsm.process( 'L1' + event.ev_subtype )
				#log( self.tname, "MAC: state after processing event " + str( self.mymac.mac_fsm.current_state ) )
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
				# print event, " ", int(round(time.time() * 1000)) 
				#log( self.tname, "MAC: state before processing event " + str( self.mymac.mac_fsm.current_state) )
				self.mymac.mac_fsm.memory = event
				self.mymac.mac_fsm.process( 'L3' + event.ev_subtype )
				#log( self.tname, "MAC: state after processing event " + str( self.mymac.mac_fsm.current_state ) )
			
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
			print "MAC: L1 event arrives at the fsm controller ", event, " ", int(round(time.time() * 1000)) 
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
    print tname + " " + msg
    
if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
