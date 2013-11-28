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



if __name__ == '__main__':
    import doctest
    doctest.testmod()

