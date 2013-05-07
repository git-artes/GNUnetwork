#!/usr/bin/env python
# -*- coding: utf-8 -*-

# frames : general classes and functions to handle generic data communication packets or frames.

'''Classes and functions for generic frames.

@var FieldTemplate: a collections.namedtuple subclass for naming metadata items on fields; 'beg', 'end' are list positions for slicing, 'inv' inverts bits if True, 'fmt' is the struct mask for packing, 'btmsk' is a bitmask for bit fields.

'''

import os
import struct
from collections import namedtuple


FieldTemplate = namedtuple('FieldTemplate', ['beg', 'end', 'inv', 'fmt', 'btmsk'])


def bin2(bb, bitlen=8, with0b=False):
    '''Converts a number into a binary string with 0 padding for a specified length.
    
    Unlike builtin function bin(), this function pads with left '0' to reach the specified length in the returned binary string. Default length is 8, excluding initial '0b'.
    @param bitlen: length of binary string to return; default 8.
    @param with0b: if True, starts binary string with '0b'; default False.
    @return: a binary string of specified length.
    '''
    if with0b:
        return '0b' + '0'*(bitlen-len(bin(bb)[2:])) + bin(bb)[2:]
    else:
        return '0'*(bitlen-len(bin(bb)[2:])) + bin(bb)[2:]

def mkbm(beg, end, bm_len, as_int=True):
    '''Make a bitmask, optionally return as int.
    
    @param beg: start position of sequence of 1s.
    @param end: end position of senquende of 1s plus 1, for correct slicing.
    @param bm_len: total length of bitmask.
    @param as_int: if True, return an int, otherwise return a binary string. Default True.
    @return: a bitmask, as a binary string or as int (the default).
    '''
    if as_int:
    	return int('0b' + '0'*(beg) + '1'*(end - beg) + '0'*(bm_len - end), 2)
    else:
       	return '0'*(beg) + '1'*(end - beg) + '0'*(bm_len - end)




class Frame():
    '''A class to represent a general data communication frame or packet.
    
    An instantiation of this class with adequate values in member variables will represent a particular type of frame, such as a MAC frame, of the Frame Control field of a MAC frame, or any other type of frame. This class assumes a frame is a sequence of bytes which can be decomposed in a series of fields where different type of data are contained. Some variable members in this class describe these fields, and some others record the actual values for each field. This class allows the packing of data into a frame, and the unpacking of data from a frame.
    Field frontiers may be byte or bit defined; a variable member defines this.
    
    TODO: for bit fields, there may be a limit size; verify this, state limit.
    
    @ivar bitbyte: if 'bytes', fields are extracted as bytes; if 'bits' fields are extracted as bits.
    @ivar ls_fields: a list of field names used to display them in a usual order.
    @ivar dc_fields: dc_fields: a dictionary {field: tuple}, tuple defines field structure. The dictionary of fields in frame describes the position, structure, and type of data kept in each field. Key is field name, value is a named tuple (begin, end, inv, type of data, bitmask); bitmask is used to extract bit fields; begin, end indicate positions of field in packed frame; inv is True if bits or bytes in field must be inverted for packing and unpacking; type indicates on which type each field is to be unpacked.
    @ivar dc_fldvals: a dictionary {field: value}; the key is the field name, value is the content in bytes of this field.
    [Check these lengths for redundancy! Some may be calculated.]
    @ivar frame_len: length of this frame.
    @ivar mask_len: length of mask ( [fixed length] frame in bytes).
    @ivar max_frame_len: maximum admitted frame length.
    @ivar body_len: actual frame body length.
    '''
    #@ivar fixed_frame_len: length of fixed length part of frame; the sum of all fixed length fields in frame.

    def __init__(self, bitbyte, frame_len, mask_len, ls_fields, dc_fields, max_frame_len=40, \
            dc_fldvals=None):     #fixed_frame_len=40, 
        '''Constructor.
        '''
        self.bitbyte = bitbyte
        self.mask_len = mask_len       # in bits, for bitbyte == 'bits'
        self.frame_len = frame_len     # in bytes, this frame length
        self.max_frame_len = max_frame_len
        #self.fixed_frame_len = fixed_frame_len
        self.ls_fields = ls_fields

        #print 'bitbyte:', bitbyte, self.bitbyte

        self.mkdcfields(dc_fields)    # makes self.dc_fields dictioary
 
        if dc_fldvals:
            self.dc_fldvals = dc_fldvals
        else:
            self.dc_fldvals = {}
            self.fillfldvals()
        
        return


    def mkdcfields(self, dc_fields):
        '''Makes a dictionary of field structure using named tuples as values.
        
        @param dc_fields: a dictionary {field: tuple}, tuple defines field structure.
        '''
        self.dc_fields = {}
        for fld in dc_fields.keys():  # load bitmask as first in template tuple
            beg, end, inv, fmt = dc_fields[fld]
            if self.bitbyte == 'bits':     #or 'b':
                btmsk = mkbm(beg, end, self.mask_len, as_int=True)
            else:
                btmsk = 'bytes, no bitmask'
            self.dc_fields[fld] = FieldTemplate(beg, end, inv, fmt, btmsk)   # named tuple with bitmask
        return

    
    def fillfldvals(self, fillchr='0'):
        '''Fill values in {field : value} dictionary with int or character.
        
        For byte fields, values are filled according to length and type of data in fields dictionary. For bit fields, values are set to 0.
        @param fillchr: the fill character, defaults to '0'.
        '''
        if self.bitbyte == 'bytes':
            for fld in self.ls_fields:
                fillval = fillchr * (self.dc_fields[fld].end - self.dc_fields[fld].beg) 
                self.dc_fldvals[fld] = fillchr
        else:
            for fld in self.ls_fields:
                self.dc_fldvals[fld] = 0
        return
        
    def consistchk(self):
        '''Run a consistency check on var members.
        
        @return: True if success, False if errors.
        '''
        pass
        
    def updtfldvals(self, dc_fldvals):
        '''Update frame with new values.
        
        @param dc_fldvals: a dictionary {field: value}.
        '''
        self.dc_fldvals.update(dc_fldvals)
        return


    def prt_dc_fields(self):
        '''Print dictionary of {field: template}.
        '''
        for fld in self.ls_fields:
            if self.bitbyte == 'bits':
                print '%10s: %s' % ( fld, bin2(self.dc_fields[fld].btmsk, self.mask_len) ) ,
                print '%4d %4d %6s %6s' % self.dc_fields[fld][:-1]
            else:
                print '%10s: %s' % ( fld, self.dc_fields[fld].btmsk ) ,
                print '%4d %4d %6s %6s' % self.dc_fields[fld][:-1]
        return
        
    def prt_dc_fldvals(self, dc_fldvals=None):
        '''Print dictionary of {field: value}.
        
        @param dc_fldvals: optional dictionary {field: value} to print; if None var member (self) dictionary is printed.
        '''
        if dc_fldvals:
            for fld in self.ls_fields:
                print '%10s: %s' % (fld, dc_fldvals[fld])        
        else:
            for fld in self.ls_fields:
                print '%10s: %s' % (fld, self.dc_fldvals[fld])
        return

    def mkpkt(self):
        '''Convert this frame into binary data.
        
        @return: a string of binary data (a packet).
        '''
        if self.bitbyte == 'bits':
            pkint = 0
            for fld in self.ls_fields:
                pkint = pkint | self.dc_fldvals[fld] << (self.mask_len - self.dc_fields[fld].end)
            return struct.pack('!I', pkint)[-self.frame_len:]
        else:
            pkbyts = ''
            for fld in self.ls_fields:
                try:
                    pkbyts = pkbyts + struct.pack(self.dc_fields[fld].fmt, self.dc_fldvals[fld])
                except:
                    print "Frames, pack error on field:", fld
                    print "  template:", self.dc_fields[fld]
                    print "  value   :", self.dc_fldvals[fld]
            return pkbyts

    def mkdic(self, pk):
        '''Make dictionary {field: value}.
        
        This function returns a dictionary {field: value}, does not update var member dictionary.
        @param pk: the packet to decode.
        @return: a dictionary of {field: value}.
        '''
        dc_fldvals = {}
        if self.bitbyte == 'bits':
            pkt = '\x00' * (4 - self.frame_len) + pk    # to unpack as an unsigned integer
            (pkint,) = struct.unpack('!I', pkt)
            for fld in self.ls_fields:
                #self.dc_fldvals[fld] = (pkint & self.dc_fields[fld].btmsk) \
                #    >> (self.mask_len - self.dc_fields[fld].end)
                dc_fldvals[fld] = (pkint & self.dc_fields[fld].btmsk) \
                    >> (self.mask_len - self.dc_fields[fld].end)
            return dc_fldvals
        else:
            for fld in self.ls_fields:
                #(self.dc_fldvals[fld],) = struct.unpack( self.dc_fields[fld].fmt, \
                #    pk[ self.dc_fields[fld].beg : self.dc_fields[fld].end ] )
                (dc_fldvals[fld],) = struct.unpack( self.dc_fields[fld].fmt, \
                    pk[ self.dc_fields[fld].beg : self.dc_fields[fld].end ] )
            return dc_fldvals

    def mkhexfl(self, fname, data=None):
        '''Make a hex file from packet to be imported by wireshark.
        
        Creates a .bin file and a .hex file.
        @param fname: a file name.
        @param data: a string as produced by mkpkt().
        @return: the return code of system command od, which converts to hex.
        '''
        f = open(fname+'.bin', 'w')
        f.write(self.mkpkt())
        f.close()
        return os.system('cat '+fname+'.bin | od -Ax -tx1 -v > '+fname+'.hex')



if __name__ == '__main__':
    import doctest
    print "frames.py: running doctest file..."
    doctest.testfile('frames.txt')
    print "frames.py: ...done running doctest file. No messages means no errors on tests."    
    

