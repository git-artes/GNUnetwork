#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Interface for libevents library with string based test frames.

This module is an interface to the events module.

To create an event object use function C{mkevent()}. This function creates events of different types, according to the event modules imported by this module. 

To add different types of events:

    - import library of specific event type.
    - add to function mkevent as necessary.
'''

import sys
sys.path += ['..']

import events as events
# event modules, for different types of events
import evtimer
import evframes80211

#from libframes import MacFrameException as MacFrameException


# import if_frames for test function

from libframes import if_frames as if_frames


def mkevent(nickname, **kwargs):
    '''Returns an event of the given event nickname.

    @param nickname: a valid event nickname, i.e. one that is a key in dictionary of valid nicknames.
    @param kwargs: a dictionary of variables depending on the type of event. Field C{ev_dc} is a dictionary of fields and values for the corresponding event type; field C{frmpkt} is a binary packed frame.
    
    >>> ev_ob_frm = mkevent('CtrlCTS')
    >>> print ev_ob_frm
    Event class name: EventFrame
      Nickname: 'CtrlCTS'; Type: 'Ctrl'; SubType: 'CTS'
      src_addr: None
      peerlinkId: 0
      payload: None
      duration: 10
      frame_length: 50
      dst_addr: None
      Frame packet: 
    >>> ev_mg = mkevent('ActionOpen', ev_dc={'src_addr':'aaaa', 'dst_addr':'bbbb', 'peerLinkId':'the peer link ID'})
    >>> print ev_mg
    Event class name: EventFrameMgmt
      Nickname: 'ActionOpen'; Type: 'Mgmt'; SubType: 'Action'
      src_addr: aaaa
      peerlinkId: 0
      payload: None
      peerLinkId: the peer link ID
      duration: 10
      frame_length: 50
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


def mkeventfromfrmobj(frmobj):
    '''Make an event from a Frame object.
    
    @param frmobj: a Frame object.
    @return: an Event object.
    '''
    # determine frame type; if Action, determine type of action frame
    if frmobj.frmtype == 'Action':
        act = frmobj.dc_frbd_fldvals['Action']
        if act == 1:
            nickname = 'ActionOpen'
        elif act == 2:
            nickname = 'ActionConfirm'
        elif act == 3:
            nickname = 'ActionClose'
        else:
          #raise MacFrameException('invalid Action field code: ' + act)
          print 'error in action field'
          return
        pass
    else:
        frmname = evframes80211.dc_frametoev[frmobj.nickname]

    # make event
    ev = mkevent(nickname)
    # set event values
    #ev.nickname = ActionConfirm
    #ev.ev_type = Mgmt
    #ev.ev_subtype = Action
    ev.ev_dc.update(frmobj.dc_fldvals)
    return ev




def test():
    '''A testing function for this module.
    '''
    print '=== ActionOpen event'
    ev_actopen = mkevent('ActionOpen')
    print ev_actopen
    print '--- Action Open frame packet'
    ev_actopen.frmpkt = ev_actopen.mkframepkt()
    print repr(ev_actopen.frmpkt)
    print '--- Action Open frame object'
    frmobj = if_frames.objfrompkt(ev_actopen.frmpkt)
    print frmobj
    print '--- Frame body dictionary'
    print frmobj.dc_frbd_fldvals
    return
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()

    test()

