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
    'TimerTimer'      : ('Timer',  'Timer',   EventTimer     ) \
    }


def mkevent(nickname, ev_dc={}):
    '''Returns an event of the given event nickname.

    @param nickname: a valid event nickname, i.e. one that is a key in dictionary of valid nicknames.    
    >>> ev_ob_tmr = mkevent('TimerTOH')
    >>> print ev_ob_tmr
    Event class name: EventTimer
      Nickname: 'TimerTOH'; Type: 'Timer'; SubType: 'TOH'
      add_info: None
    >>> ev_ob_tmr = mkevent('TimerTOH', ev_dc={'add_info':'additional info, testing'})
    >>> print ev_ob_tmr
    Event class name: EventTimer
      Nickname: 'TimerTOH'; Type: 'Timer'; SubType: 'TOH'
      add_info: additional info, testing
      
    '''
    #if not type(eventclass) == types.ClassType:
    #    raise EventNameException('eventclass must be a class object.')
    if dc_nicknames.has_key(nickname):
        ptype, psubtype, eventclass = dc_nicknames[nickname]
        return eventclass(nickname, ptype, psubtype, ev_dc)
    else:
        raise EventNameException(nickname + ' is not a valid nickname.')


if __name__ == '__main__':
    import doctest
    doctest.testmod()


