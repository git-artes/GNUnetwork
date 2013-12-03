#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Interface for libevents library with string based test frames.

This module is an interface to the events module.

To create an event object use function C{mkevent()}. This function creates events of different types, according to the event modules imported by this module. 

To add different types of events:

    - import library of specific event type.
    - add to function mkevent as necessary.
'''

import events as events
# event modules, for different types of events
import evtimer
import evframes80211


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
    return



if __name__ == '__main__':
    import doctest
    doctest.testmod()

