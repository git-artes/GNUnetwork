#!/usr/bin/env python
# -*- coding: utf-8 -*-

# classes for events


import sys
import types

sys.path = sys.path + ['..']

from libframes import mac_api
#from libframes.mac_frcl import dc_type2str, dc_stype2str
#from libframes.mac_frcl import dc_type2num, dc_type2str, dc_stype2num, dc_stype2str

'''A module to handle events.

Events type and subtype are reserved for standard compliant denominations, such as Type and Subtype in frames. Field ev_nickname is a descriptive nomination to handle events in Finite State Machines or other; ev_nickname is a convention of this project.
Nickname: 1. A descriptive name added to or replacing the actual name of a person, place, or thing (American Heritage Dictionary).

To create an event use function mkevent, like this::
  ev_ob = events.mkevent(events.EventTimer, 'TimerTOH')

The first parameter must be one of the Event subclassesd defined in this module, it is a class object. The second parameter must be one of the nicknames defines for the different kinds of events.

@var dc_nicknames: a dictionary {nickname: (type, subtype) } of valid nicknames and their corresponding type and subtype.
'''

# a dictionary of nicknames, types and subtypes
#   nickname          :  (type,     subtype )
dc_nicknames = { \
    'CtrlRTS'         : ('Ctrl',   'RTS'   ), \
    'CtrlCTS'         : ('Ctrl',   'CTS'   ), \
    'CtrlACK'         : ('Ctrl',   'ACK'   ), \
    'DataData'        : ('Data',   'Data'  ), \
    'ActionOpen'      : ('Mgmt',   'Action'), \
    'ActionClose'     : ('Mgmt',   'Action'), \
    'ActionConfirm'   : ('Mgmt',   'Action'), \
    'MgmtBeacon'      : ('Mgmt',   'Beacon'), \
    'TimerTOH'        : ('Timer',  'TOH'   ), \
    'TimerTOC'        : ('Timer',  'TOC'   ), \
    'TimerTOR1'       : ('Timer',  'TOR1'  ), \
    'TimerTOR2'       : ('Timer',  'TOR2'  ) \
    }

    
def mkevent(eventclass, pnickname):
    '''Returns an event of the given eventclass, eventnickname.
    
    @param eventclass: an event class object, one of the classes defined in this module.
    @param pnickname: a valid event nickname, i.e. one that is a key in dictionary of valid nicknames.
    '''
    if not type(eventclass) == types.ClassType:
        raise EventNameException('eventclass must be a class object.')
    if dc_nicknames.has_key(pnickname):
        ptype, psubtype = dc_nicknames[pnickname]
        return eventclass(pnickname, ptype, psubtype)
    else:
        raise EventNameException(pnickname + ' is not a valid nickname.')



class Event:
    '''A general class for all types of event.
    '''

    def __str__(self):
        return "Event Nickname: '%s'; Type: '%s'; SubType: '%s'"  % \
            ( self.ev_nickname, self.ev_type, self.ev_subtype)


class EventFrame(Event):
    '''An event associated with a frame.
    
    @ivar ls_nicknames: a list of recognized nicknames.
    '''

    def __init__(self, pnickname, ptype, psubtype, pfrmpkt=''):
        '''Constructor.
        
        Frame event type and subtype must be valid frame type and subtype.
        @param pnickname: a descriptive name for this event.
        @param ptype: frame event type.
        @param psubtype: frame event subtype
        @param pfrmpkt: a packed frame in bin format, as for transmission.
        '''
        self.ev_nickname = pnickname
        self.ev_type = ptype
        self.ev_subtype = psubtype
        frmpkt = pfrmpkt
        return



class EventTimer(Event):
    '''An event associated with a timer.
    '''
    
    def __init__(self, pnickname, ptype, psubtype, add_info=None):
        '''Constructor.

        @param pnickname: a descriptive name for this event.
        @param ptype: timer event type.
        @param psubtype: timer event subtype.
        @param add_info: additional info.
        '''
        self.ev_nickname = pnickname
        self.ev_type = ptype
        self.ev_subtype = psubtype
        if add_info:
            self.add_info = add_info
        return


class EventNameException(Exception):
    '''An exception to rise on non valid parameters for event construction.
    '''
    pass        


if __name__ == '__main__':

    print '== Events. Dictionary of nicknames, type and subtype:'
    for key in dc_nicknames.keys():
        ev_type, ev_subtype = dc_nicknames[key]
        print '  %s : %s, %s' % \
            (key.ljust(20), ev_type.ljust(20), ev_subtype.ljust(20))

    print '== Make a timer event object using:'
    print "  ev_ob = events.mkevent(events.EventTimer, 'TimerTOH')"
    ev_ob = mkevent(EventTimer, 'TimerTOH')
    print "== Print event object data with 'print ev_ob':"
    print ev_ob
   

