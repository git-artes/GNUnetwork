#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Use of events with string frames.

This module defines two functions, mkevent() to make an Event object from a nickname and frame, and mkframe() to make a string frame from an Event object.
'''

import events
import if_events
import sys


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
        return if_events.mkevent(pnickname, ev_dc={'src_addr':'', 'dst_addr':''})
    if pframe:
        #print "evstrframes.frame:", pframe
        ev_dc = {}
        nickname, ev_dc  = pframe.split(',',1)
        print ev_dc
        try:
            ev = if_events.mkevent(nickname, frmpkt=pframe, ev_dc=eval(ev_dc))
        except:
            print "Cannot generates event: malformed packet"
            ev =None
        #ev.src_addr=src_addr
        #ev.dst_addr = dst_addr
        #print "evstrframes.mkevent:"
        #print ev
        return  ev


def mkframe(ev_obj):
    '''Returns a frame with the event information.
    
    @param ev_obj: an Event object.
    @return: a frame in bin data format (confirm!).
    '''
    if not isinstance(ev_obj, events.Event):
        raise EventNameException('Parameter is not an Event object.')
        return None
    if not ev_obj.ev_dc:
        raise EventNameException('ev_dc not in event object.')
    if not ev_obj.ev_dc.has_key('src_addr') or not ev_obj.ev_dc.has_key('dst_addr'):
        raise EventNameException('ev_dc does not contain src_addr, dst_addr keys.')
    if not ev_obj.nickname:
        raise EventNameException('even with no nickname.')
    #print 'evstrframes.mkframe, event object:'
    if not ev_obj.ev_dc['src_addr']:
        ev_obj.ev_dc['src_addr'] = ''
    if not ev_obj.ev_dc['dst_addr']:
        ev_obj.ev_dc['dst_addr'] = ''
    if not ev_obj.ev_dc['peerlinkId']:
        ev_obj.ev_dc['peerlinkId'] = 0
    #print ev_obj
    frame = "" + ev_obj.nickname + "," + str(ev_obj.ev_dc)
    #print frame
    #sys.exit()
    return frame


def test():
    ev = if_events.mkevent("MgmtBeacon", ev_dc={})
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
        


