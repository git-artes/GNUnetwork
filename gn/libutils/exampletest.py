#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A module to show the use of doctest in testing.

Instructions to use:

    1. Write module.
    2. Write text file for testing; see exampletext.txt for a worked out example.
    3. Test module by executing::
        python -m doctest exampletext.txt
        
A usual naming convention is to name the doctest file as the module, but with extension 'txt': doctest file for thid module C{exampletest.py} is named C{exampletest.txt}.

To include execution of tests in this module's main, include the following lines::

    import sys
    ...
    if __name__ == '__main__':
        import doctest
        testfilename = sys.argv[0].rpartition('.')[0] + '.txt'
        try:
            doctest.testfile(testfilename)
        except:      # no text file present
            pass
    
'''

import sys

class AClass:
    def __init__(self, par1):
        self.par1 = par1
    def __str__(self):
        return 'Object from class ' + str(self.__class__) + \
            ', value: ' + str(self.par1)


if __name__ == '__main__':
    import doctest
    testfilename = sys.argv[0][:-2] + 'txt'
    try:
        doctest.testfile(testfilename)
    except:      # no text file present
        pass


