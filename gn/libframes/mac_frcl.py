#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Classes and functions for MAC Frame Control field.

@var ls_types: list of tuples (number code, name) for frame types.
@var ls_subtypes: list of tuples (number_code, name) for frame subtypes.
@var dc_type2str: dictionary of {number_code, name} for frame types.
@var dc_type2num: dictionary of {name, number_code} for frame types.
@var dc_stype2str: dictionary of {number_code, name} for frame subtypes.
@var dc_stype2num: dictionary of {name, number_code} for frame subtypes.

'''

import struct
import frames
from frames import Frame

"""
# Frame Types, dictionary initialization
ls_types = [ (0, 'Mgmt'), (1, 'Ctrl'), (2, 'Data'), (3, 'Reserved') ]
dc_type2str, dc_type2num = {}, {}
for (nn, ss) in ls_types:
    dc_type2str[nn] = ss
    dc_type2num[ss] = nn
# Frame SubTypes, dictionary initialization
ls_subtypes = [ (8, 'Beacon'), (11, 'RTS'), (12, 'CTS'), (13, 'ACK'), (0,'Data') ]
dc_stype2str, dc_stype2num = {}, {}
for (nn, ss) in ls_subtypes:
    dc_stype2str[nn] = ss
    dc_stype2num[ss] = nn
"""

dc_typesbycode = { \
    ( 0, 8) : ('Mgmt', 'Beacon'), \
    ( 1,11) : ('Ctrl', 'RTS'), \
    ( 1,12) : ('Ctrl', 'CTS'), \
    ( 1,13) : ('Ctrl', 'ACK'), \
    ( 2, 0) : ('Data', 'Data') \
    }
dc_typesbyname = {}
for key in dc_typesbycode.keys():
    dc_typesbyname[dc_typesbycode[key]] = key




class FCframe(Frame):
    '''Frame Control field (FC) for MAC frame.
    
    A class to define frame control field in MAC frames.
    @ivar dc_frmtype: a dictionary of frame types. Keys are frame type names, e.g. 'RTS', 'DATA'; values are a dictionary {'ProtVer':<int>, 'Type':<int>, 'SubType':<int>} which define the field values in frame control for the required frame type.
    '''
    dc_frmtype = { \
        'RTS'   : {'ProtVer':0, 'Type':1, 'SubType':11}, \
        'CTS'   : {'ProtVer':0, 'Type':1, 'SubType':12}, \
        'ACK'   : {'ProtVer':0, 'Type':1, 'SubType':13}, \
        'DATA'  : {'ProtVer':0, 'Type':2, 'SubType':0}, \
        'Beacon': {'ProtVer':0, 'Type':0, 'SubType':8}, \
        'Action': {'ProtVer':0, 'Type':0, 'SubType':13} \
        }
        
    def __init__(self, dc_fldvals={}):
        '''Builds an FCframe object updating field values of frame control fields.
        
        @param dc_fldvals: a dictionary of {field: value} to update field values.
        '''
        self.bitbyte = 'bits'
        self.frame_len = 2
        self.mask_len = 16

        self.ls_fields= ['ProtVer', 'Type', 'SubType', 'ToDS', 'FromDS', 'MoreFrags', \
            'Retry', 'PwrMgmt', 'MoreData', 'Protected', 'Order']
        dc_fields      = { \
            'ProtVer'  : ( 6,  8, 0,     'int'  ), \
            'Type'     : ( 4,  6, 0,     'int'  ), \
            'SubType'  : ( 0,  4, 0,     'int'  ), \
            'ToDS'     : (15, 16, False, 'bool' ), \
            'FromDS'   : (14, 15, False, 'bool' ), \
            'MoreFrags': (13, 14, False, 'bool' ), \
            'Retry'    : (12, 13, False, 'bool' ), \
            'PwrMgmt'  : (11, 12, False, 'bool' ), \
            'MoreData' : (10, 11, False, 'bool' ), \
            'Protected': ( 9, 10, False, 'bool' ), \
            'Order'    : ( 8,  9, False, 'bool' )  \
             }
        """dc_fields      = { \
            #'ProtVer'  : ( 0,  2, 0,     'int'  ), \
            #'Type'     : ( 2,  4, 0,     'int'  ), \
            #'SubType'  : ( 4,  8, 0,     'int'  ), \
            'ProtVer'  : ( 6,  8, 0,     'int'  ), \
            'Type'     : ( 4,  6, 0,     'int'  ), \
            'SubType'  : ( 0,  4, 0,     'int'  ), \

            'ToDS'     : ( 8,  9, False, 'bool' ), \
            'FromDS'   : ( 9, 10, False, 'bool' ), \
            'MoreFrags': (10, 11, False, 'bool' ), \
            'Retry'    : (11, 12, False, 'bool' ), \
            'PwrMgmt'  : (12, 13, False, 'bool' ), \
            'MoreData' : (13, 14, False, 'bool' ), \
            'Protected': (14, 15, False, 'bool' ), \
            'Order'    : (15, 16, False, 'bool' )  \
             }"""
        self.mkdcfields(dc_fields)
        self.dc_fldvals = {}
        self.fillfldvals()
        self.dc_fldvals.update(dc_fldvals)        # add field values from parameter

    def setfctype(self, frmtype):
        '''Sets frame control values for a certain frame type.
        
        @param frmtype: a frame type.
        '''
        if FCframe.dc_frmtype.has_key(frmtype):
            self.dc_fldvals.update( FCframe.dc_frmtype[frmtype] )
        else:
            print 'setfctype: wrong frame type', frmtype
        return

    def getfcint(self):
        '''Get frame control value as an 2-byte int.
        '''
        pkint = 0
        for fld in self.ls_fields:
            pkint = pkint | self.dc_fldvals[fld] << \
                (self.mask_len - self.dc_fields[fld].end)
        return pkint


