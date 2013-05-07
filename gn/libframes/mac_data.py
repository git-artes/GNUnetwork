#!/usr/bin/env python
# -*- coding: utf-8 -*-

# mac_data.py

'''Classes and functions for MAC Data frames.
'''

import frames
from frames import Frame
from mac_frcl import FCframe


class DATAframe(Frame):
    '''DATA MAC frame.
    '''
    def __init__(self, dc_fldvals={}):
        '''Builds a DATAframe object, updating field values for DATA MAC frame.
        
        @param dc_fldvals: a dictionary of {field: value} to update field values.
        '''    
        self.bitbyte='bytes'
        self.frame_len = 14
        self.mask_len = 0    # bytes, no bitmask
        self.ls_fields= ['frame_ctrl', 'duration', 'address_1', 'address_2', \
            'address_3', 'seq_ctrl', 'qos', 'ht', 'address_4', 'frame_body', 'fcs']
        dc_fields =  {\
            'frame_ctrl' : ( 0,  2,   False,   '!H' ), \
            'duration'   : ( 2,  4,   False,   '!H'  ), \
            'address_1'  : ( 4, 10,   False,   '!6s' ), \
            'address_2'  : (10, 16,   False,   '!6s' ), \
            'address_3'  : (16, 22,   False,   '!6s' ), \
            'seq_ctrl'   : (22, 24,   False,   '!H'  ), \
            'qos'        : (24, 26,   False,   '!H'  ), \
            'ht'         : (26, 30,   False,   '!I'  ), \
            'address_4'  : (30, 36,   False,   '!6s' ), \
            'frame_body' : (36, 2342, False,   '!s'  ), \
            'fcs'        : (-4, None, False,   '!I'  )   \
            }
        self.mkdcfields(dc_fields)
        self.adjdatalen(dc_fldvals)        # adjust dc_fields template for data length
        self.dc_fldvals =  {  \
            'frame_ctrl' : 0, \
            'duration'   : 0, \
            'address_1'  : 'dt-ad1-', \
            'address_2'  : 'dt-ad2-', \
            'address_3'  : 'dt-ad3-', \
            'seq_ctrl'   : 0, \
            'qos'        : 0, \
            'ht'         : 0, \
            'address_4'  : 'dt-ad2-', \
            'frame_body' : 'generic frame body', \
            'fcs'        : 0 \
            }
        # set values for Data frame in Frame Control field
        #fc_obj = FCframe()
        #fc_obj.setfctype('DATA')
        #self.dc_fldvals.update( {'frame_ctrl':fc_obj.mkpkt()} )
        self.dc_fldvals.update( FCframe.dc_frmtype['DATA'] )
        self.dc_fldvals.update(dc_fldvals)
        return

    def adjdatalen(self, dc_fldvals):
        '''Adjust for variable length frame_body field.
        
        @param dc_fldvals: a dictionary {field: value}.
        '''
        if dc_fldvals.has_key('frame_body'):
            self.frame_len = 40 + len(dc_fldvals['frame_body'])
        else:
            self.frame_len = 40    # null data frame
        self.dc_fields['frame_body'] = frames.FieldTemplate(36, self.frame_len-4, \
            False, '!'+str(self.frame_len-4-36)+'s', 'frame_body, bytes')
        self.dc_fields['fcs']        = frames.FieldTemplate(self.frame_len-4, \
            self.frame_len,  False, \
            '!I', 'fcs, bytes       ')
        return

    def updtfldvals(self, dc_fldvals):
        '''Update frame with new values.
        
        @param dc_fldvals: a dictionary {field: value}.
        '''
        self.adjdatalen(dc_fldvals)   # adjust dc_fields template for data length
        self.dc_fldvals.update(dc_fldvals)
        return
        

    def mkdic(self, pk):
        '''Make dictionary {field: values} adjusting length of frame body.
        
        Overwrites super function to adjust length of frame body in data packet.
        @param pk: the packet to decode.
        @return: a dictionary of {field: value}.
        '''
        self.adjdatalen( { 'frame_body': pk[36:(len(pk)-4)] } )
        #self.prt_dc_fields()
        return Frame.mkdic(self, pk)


if __name__ == '__main__':
    import doctest
    print "mac_data.py: running doctest file..."
    doctest.testfile('mac_data.txt')
    print "mac_data.py: ...done running doctest file. No messages means no errors on tests."
    
