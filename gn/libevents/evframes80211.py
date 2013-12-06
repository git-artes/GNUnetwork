#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Classes and functions to handle events from and to IEEE 802.11 frames.

@var dc_nicknames: a dictionary of nicknames, types, subtypes, and classnames, C{ {nickname: (type, subtype, classname)} }; C{classname} is the class used to build the object. This dictionary allows to build a frame event object by just saying its nickname. Module function C{mkevent()} uses this module variable.
'''

from events import Event, EventNameException



class EventFrame(Event):
    '''An event associated with a frame.
    
    @ivar nickname: a descriptive name for this event.
    @ivar ev_type: frame event type.
    @ivar ev_subtype: frame event subtype.
    @ivar frmpkt: a packed frame in bin format, as for transmission.
    @ivar ev_dc: a dictionary of complementary data, e.g. {'src_addr': source address, 'dst_addr': destination address, 'duration': duration}.
    '''

    def __init__(self, nickname, ev_type, ev_subtype, frmpkt=None, ev_dc={}):
        '''Constructor.
        '''
        self.nickname = nickname
        self.ev_type = ev_type
        self.ev_subtype = ev_subtype
        self.frmpkt = frmpkt
        self.ev_dc = { \
            'src_addr': None, \
            'dst_addr': None, \
            'duration': 10, \
            'frame_length': 50, \
            'peerlinkId': 0, \

            }
        self.ev_dc.update(ev_dc)
        return

    def __str__(self):
        ss = Event.__str__(self)
        ss += '\n  Frame packet: ' + str(self.frmpkt)
        return ss



class EventFrameMgmt(EventFrame):

    def __init__(self, nickname, ev_type, ev_subtype, frmpkt=None, ev_dc={}):
        '''Constructor.
        '''
        EventFrame.__init__(self, nickname, ev_type, ev_subtype, \
            frmpkt=frmpkt, ev_dc=ev_dc)
       


dc_nicknames = { \
    'CtrlRTS'         : ('Ctrl',   'RTS',     EventFrame     ), \
    'CtrlCTS'         : ('Ctrl',   'CTS',     EventFrame     ), \
    'CtrlACK'         : ('Ctrl',   'ACK',     EventFrame     ), \
    'DataData'        : ('Data',   'Data',    EventFrame     ), \
    'ActionOpen'      : ('Mgmt',   'Action',  EventFrameMgmt ), \
    'ActionClose'     : ('Mgmt',   'Action',  EventFrameMgmt ), \
    'ActionConfirm'   : ('Mgmt',   'Action',  EventFrameMgmt ), \
    'MgmtBeacon'      : ('Mgmt',   'Beacon',  EventFrameMgmt ), \
    }


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
