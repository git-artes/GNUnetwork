#!/usr/bin/env python
# -*- coding: utf-8 -*-

# classes for events


import sys
sys.path = sys.path + ['..']
from libframes.mac_frcl import dc_type2num, dc_type2str, dc_stype2num, dc_stype2str

from libframes import mac_api
from libframes.mac_frcl import dc_type2str, dc_stype2str

# List of Timer Events
ls_timertypes = ['Timer']    # only one, for the time being
ls_timersubtypes = ['TOH', 'TOC', 'TOR1', 'TOR2']        # add as necessary


class Event:
    '''A general class for all types of event.
    '''
    ev_type = ''
    ev_subtype = ''

    def __str__(self):
        return 'Type: %s; SubType: %s' % (self.ev_type, self.ev_subtype)



class EventFrame(Event):
    '''An event associated with a frame.

    @ivar ev_type: the type of event.
    @ivar ev_subtype: the subtype of event.
    '''

    def __init__(self, ptype='', psubtype='', frmpkt=''):
        '''Constructor.
        
        Frame event type and subtype must be registered as keys in the corresponding dictionaries dc_type2num, dc_stype2num. Otherwise, object is created but type or subtype is left as the empty string.
        @param ptype: frame event type.
        @param psubtype: frame event subtype
        '''
        if ptype and dc_type2num.has_key(ptype):
            self.ev_type = ptype
        if psubtype and dc_stype2num.has_key(psubtype):
            self.ev_subtype = psubtype
        if frmpkt:
            self.frmtype, self.fc_dic, self.fr_dic = \
                mac_api.mkdics(frmpkt)
            nm_type, nm_stype = self.fc_dic['Type'], self.fc_dic['SubType']
            self.ev_type = dc_type2str[nm_type]
            self.ev_subtype = dc_stype2str[nm_stype]


class EventTimer(Event):
    '''An event associated with a timer.

    @ivar add_info: additional information; default None.
    @ivar ev_type: timer event type.
    @ivar ev_subtype: timer event subtype
    '''
    def __init__(self, ptype='', psubtype='', add_info=None):
        '''Constructor.
        
        Timer event type and subtype must be registered in the corresponding lists, ls_timertypes, ls_timersubtypes. Otherwise, object is created but type or subtype is left as the empty string.
        @param ptype: timer event type.
        @param psubtype: timer event subtype
        '''
        if ptype and ptype in ls_timertypes:
            self.ev_type = ptype
        if psubtype and psubtype in ls_timersubtypes:
            self.ev_subtype = psubtype
        self.add_info = add_info



