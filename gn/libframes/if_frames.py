#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''An API to the IEEE 802.11 frame library.
'''

import mac_frmbld
import mac_frmspecs


def objfrompkt(frmpkt):
    '''Create a frame object from a binary string format frame.
    
    @param frmpkt: a frame in binary string format.
    @return: a frame object.
    '''
    return mac_frmbld.mkfrmobj(frmpkt)


def pktfromobj(frmobj):  # pack
    '''Create a frame in binary string format from a frame object.
    
    @param frmobj: a frame object.
    @return: a frame in binary string format.
    '''
    return frmobj.mkpkt()


def mkframeobj(frmname, dc_frcl_fldvals={}, dc_fldvals={}, dc_frbd_fldvals={} ):
    '''Create a frame object from a nickname and dictionary of fields.

    @param frmtype: a conventional name for the type of frame.
    @param dc_frcl_fldvals: a dictionary of {field: value} to update dictionary of field values in Frame Control field.
    @param dc_fldvals: a dictionary of {field: value} to update dictionary of field values in this frame.
    @param dc_frbd_fldvals: a dictionary of {field: value} to update dictionary of field values in frame body.
    @return: a frame object.
    '''
    return mac_frmbld.AFrame(frmname, dc_frcl_fldvals={}, dc_fldvals={}, \
        dc_frbd_fldvals={} )

 
def showfldvals(frmobj):
    '''Show values for all fields in a frame object.
    
    @param frmobj: a frame object.
    '''
    return mac_frmspecs.showfields(frmobj)


def showfieldnames(frmname):
    '''Show all field names for a frame object of given frame name.
    
    @param frmname: a frame name.
    '''
    frmclass, frmbodyclass = mac_frmspecs.getfrmclass(frmname)
    print '== Fields for object name: ' + frmname
    print '-- Frame field names:'
    print frmclass.ls_fields
    if frmbodyclass:
        print '-- Frame body field names:'
        print frmbodyclass.ls_fields
    print '==\n'


def test():
    '''A test function for the frames interface.

    For the types of frame known, create a frame object, pack it into binary string format, create a second frame object from the packed frame.
    '''
    ls_known = ['Beacon', 'RTS', 'CTS', 'ACK', 'Data', 'Action']
    for frtype in ls_known:
        print '==== %15s ... ' % (frtype.ljust(15),),
        try:
            ob = mkframeobj(frtype)
        except:
            print ' Object creation Error'        
        try:
            pk_ob = pktfromobj(ob)
        except:
            print ' Packing error'
        try:
            ob2 = objfrompkt(pk_ob)
        except:
            print 'Unpacking error'
            continue
        print 'OK'
    return


if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass


