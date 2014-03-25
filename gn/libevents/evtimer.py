#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Classes and functions to handle events for timing.

@var dc_nicknames: a dictionary of nicknames, types, subtypes, and classnames, C{ {nickname: (type, subtype, classname)} }; C{classname} is the class used to build the object. This dictionary allows to build a time event object by just saying its nickname. Module function C{mkevent()} uses this module variable.
'''

from events import Event, EventNameException



class EventTimer(Event):
    '''An event associated with a timer.
    
    @ivar nickname: a descriptive name for this event.
    @ivar ev_type: timer event type.
    @ivar ev_subtype: timer event subtype.
    @ivar ev_dc: a dictionary of complementary data, e.g. {'add_info': 'additional information'}.
    '''
    
    def __init__(self, nickname, ev_type, ev_subtype, ev_dc={}):
        '''Constructor.
        '''
        self.nickname = nickname
        self.ev_type = ev_type
        self.ev_subtype = ev_subtype
        self.ev_dc = {'add_info':None}
        self.ev_dc.update(ev_dc)
        return


dc_nicknames = { \
    'TimerTOH'        : ('Timer',  'TOH',     EventTimer     ), \
    'TimerTOC'        : ('Timer',  'TOC',     EventTimer     ), \
    'TimerTOR1'       : ('Timer',  'TOR1',    EventTimer     ), \
    'TimerTOR2'       : ('Timer',  'TOR2',    EventTimer     ), \
    'TimerTimer'      : ('Timer',  'Timer',   EventTimer     ), \
	'TimerCTSTout'    : ('Timer',  'CTSTout', EventTimer     ), \
	'TimerRTSAbort'   : ('Timer',  'RTSAbort', EventTimer     ), \
	'TimerACKTout'    : ('Timer',  'ACKTout', EventTimer     ), \
	'TimerDataAbort'  : ('Timer',  'DataAbort', EventTimer     ) \
    }



if __name__ == '__main__':
    import doctest
    doctest.testmod()


