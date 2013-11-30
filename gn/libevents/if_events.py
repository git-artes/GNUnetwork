#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Interface for libevents library with string based test frames.

This interface module defines two functions, mkevent() to make an Event object from a nickname and frame, and mkframe() to make a string frame from an Event object.

Proposed name for this module: if_events_strfrm.
'''

import events as events


def mkevent(pnickname=None, pframe=None):
    '''Creates an event from a nickname or from a frame.
    
    @param pnickname: the event nickname.
    @param pframe: a frame in bin dta format (confirm!)
    @return: an Event object.
    '''
    if not pnickname and not pframe:
        raise events.EventNameException('No nickname or frame received.')
        return None
    if pnickname:
        pass
        return  # ...an Event object
    if pframe:
        ev_dc = {}
        nickname, ev_dc['src_addr'], ev_dc['dst_addr'] = pframe.split(',')
        ev = events.mkevent(nickname, frmpkt=pframe, ev_dc=ev_dc)
        #ev.src_addr=src_addr
        #ev.dst_addr = dst_addr
        return  ev


def mkframe(ev_obj):
    '''Returns a frame with the event information.
    
    @param ev_obj: an Event object.
    @return: a frame in bin data format (confirm!).
    '''
    if not isinstance(ev_obj, events.Event):
        raise EventNameException('Parameter is not an Event object.')
        return None
    frame = "" + ev_obj.nickname + "," + \
        ev_obj.ev_dc['src_addr'] + "," + ev_obj.ev_dc['dst_addr']
    return frame


def test():
    ev = events.mkevent("MgmtBeacon", ev_dc={})
    ev.ev_dc['src_addr'] = "100"
    ev.ev_dc['dst_addr'] =  "150"
    print "=== Event to frame:"; print ev
    frame=mkframe(ev)
    print "=== Frame:", frame
    evfromframe = mkevent(pframe=frame) 
    print "=== Event from frame:"; print evfromframe
    return

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
        


