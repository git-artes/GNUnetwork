#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''An interface for the libevents library of Events.

'''

from events import *


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
        pass
        return  # ...an event object


def mkframe(ev_obj):
    '''Returns a frame with the event information.
    
    @param ev_obj: an Event object.
    @return: a frame in bin data format (confirm!).
    '''
    if not isinstance(ev_obj, Event):
        raise EventNameException('Parameter is not an Event object.')
        return None
    pass
    return



