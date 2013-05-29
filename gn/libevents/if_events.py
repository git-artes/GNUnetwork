#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''An interface for the libevents library of Events.

'''

import events as events


def mkevent(pnickname=None, pframe=None):
    '''Creates an event froma nickname or from a frame.
    
    @param nickname: the event nickname.
    @param frame: a frame in bin dta format (confirm!)
    @return: an Event object.
    '''
    if not pnickname and not pframe:
        raise EventNameException('No nickname or frame received.')
        return None
    if pnickname:
        pass
        return  # ...an Event object
    if pframe:
        nickname,src_addr,dst_addr = pframe.split(',')
        ev= events.mkevent(nickname)
        ev.src_addr=src_addr
        ev.dst_addr = dst_addr
        return  ev


def mkframe(ev_obj):
    '''Returns a frame with the event information.
    
    @param ev_obj: an Event object.
    @return: a frame in bin data format (confirm!).
    '''
    if not isinstance(ev_obj, events.Event):
        raise EventNameException('Parameter is not an Event object.')
        return None
    frame = ""+ev_obj.ev_nickname+","+ev_obj.src_addr+","+ev_obj.dst_addr
    return frame


def test():
    ev = events.mkevent("MgmtBeacon")
    ev.src_addr = "100"
    ev.dst_addr=  "150"

    frame=mkframe(ev)
    print " Frame = :", frame

    event=mkevent(pframe=frame) 
    print "Event =", event     

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
        
