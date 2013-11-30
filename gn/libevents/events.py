#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Classes and functions to handle events.

Class Event is a generic class for all types of events. Class Event is expected to be specialized into different, more specific types of events, implemented as subclasses. A hierarchy of event types and subtypes is possible. Events are distinguished by a nickname, a descriptive name used to recognize the type of event whatever their position in the event class hierarchy. Event nicknames are a convention of this project.

Nickname: 1. A descriptive name added to or replacing the actual name of a person, place, or thing (American Heritage Dictionary).

#To create an event object use function C{mkevent()}.
#@var dc_nicknames: a dictionary {nickname: (type, subtype, eventclass) } of valid nicknames, their corresponding type and subtype, and the class object used for construction.
'''

import sys
import types

sys.path = sys.path + ['..']

#from libframes.mac_frcl import dc_type2str, dc_stype2str
#from libframes.mac_frcl import dc_type2num, dc_type2str, dc_stype2num, dc_stype2str


class Event:
    '''A general class for all types of event.
    '''

    def __init__(self, nickname):
        '''Constructor.
        
        @param nickname: a descriptive name to indicate the type of event.
        '''
        self.nickname = nickname
        self.dc_ev = {}
        
    def __str__(self):
        ss = 'Event class name: ' + self.__class__.__name__
        ss += "\n  Nickname: '%s'; Type: '%s'; SubType: '%s'"  % \
            (self.nickname, self.ev_type, self.ev_subtype)
        for key in self.ev_dc.keys():
            ss += '\n  ' + key + ': ' + str(self.ev_dc[key])
        return ss

    # see if really needed, nickname is public
    def getname(self):
        return self.nickname


class EventNameException(Exception):
    '''An exception to rise on non valid parameters for event construction.
    '''
    pass 


import evtimer
import evframes80211



#def mkevent(nickname, frmpkt=None, ev_dc={}):
def mkevent(nickname, **kwargs):
    '''Returns an event of the given event nickname.

    @param nickname: a valid event nickname, i.e. one that is a key in dictionary of valid nicknames.
    
    >>> ev_ob_frm = mkevent('CtrlCTS')
    >>> print ev_ob_frm
    Event class name: EventFrame
      Nickname: 'CtrlCTS'; Type: 'Ctrl'; SubType: 'CTS'
      duration: None
      src_addr: None
      dst_addr: None
      Frame packet: 
    >>> ev_mg = mkevent('ActionOpen', ev_dc={'src_addr':'aaaa', 'dst_addr':'bbbb', 'peerLinkId':'the peer link ID'})
    >>> print ev_mg
    Event class name: EventFrameMgmt
      Nickname: 'ActionOpen'; Type: 'Mgmt'; SubType: 'Action'
      src_addr: aaaa
      duration: None
      peerLinkId: the peer link ID
      dst_addr: bbbb
      Frame packet: 
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
    #if dc_nicknames.has_key(nickname):
    #    ev_type, ev_subtype, eventclass = dc_nicknames[nickname]
    #    return eventclass(nickname, ev_type, ev_subtype, frmpkt, ev_dc)
    #else:
    #    raise EventNameException(nickname + ' is not a valid nickname.')

    frmpkt, ev_dc = '', {}
    if kwargs.has_key('ev_dc'):
        ev_dc = kwargs['ev_dc']
    if kwargs.has_key('frmpkt'):
        frmpkt = kwargs['frmpkt']
        
    if evtimer.dc_nicknames.has_key(nickname):
        ptype, psubtype, eventclass = evtimer.dc_nicknames[nickname]
        return eventclass(nickname, ptype, psubtype, ev_dc)    
    elif evframes80211.dc_nicknames.has_key(nickname):
        ev_type, ev_subtype, eventclass = evframes80211.dc_nicknames[nickname]
        return eventclass(nickname, ev_type, ev_subtype, frmpkt, ev_dc)
    else:
        raise EventNameException(nickname + ' is not a valid nickname.')




if __name__ == '__main__':
    import doctest
    doctest.testmod()

