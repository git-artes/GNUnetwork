#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A logger for the GNU Network modules.

This module provides configuration for the logging facilities used in the GNU network modules.

See:  See I{"Logging", "Logging HowTo", and "Logging Cookbook" in Python Documentation}.

@var appname: application name, default 'GNlogger'.
@var fname: log file name, default 'gnlogger.log'.
@var fmode: log file mode, default 'w'. Mode 'a' appends to existing file, mode 'w' starts a new log file.
@var loglvl: less sever log level to start logging, default DEBUG. In increasing order of severity: DEBUG, INFO, WARNING, ERROR, CRITICAL. Default C{logging.DEBUG}. See I{Logging HowTo} in Python Documentation.
@var fmtstr: format string to define format of log output.
@var logdir: directory to place log files, defaults to C{../logs}.
'''

import logging
import gnlogger_test

# set default behavior, initialize variables
appname = 'GNlogger'    
fname = 'gnlogger.log'   # log file name
fmode = 'w'              # log file mode, 'a' for append, 'w' restarts
loglvl = logging.DEBUG   # log level
fmtstr = '%(asctime)s %(levelname)s %(name)s: %(message)s'
logdir = '../logs/'      # set to './' to log to current directory

def logconf(app=appname, fnm=fname, fmd=fmode, lvl=loglvl, fmt=fmtstr, \
        lgd=logdir):
    '''Configures the logging system.
    
    @param app: application name.
    @param fnm: log file name.
    @param fmd: log file mode.
    @param lvl: log level.
    @param fmt: format string for logging output.
    @param lgd: log directory.
    '''
    logging.basicConfig(filename=lgd+fnm, filemode=fmd, level=lvl, \
        format=fmt)
    logger = logging.getLogger(app)
    logger.info('logging configured')

    return

if __name__ == '__main__':
    '''Configures logging, does some testing using another module.
    '''

    logconf()
    logger = logging.getLogger(__name__)
    logger.info('in gnlogger main')

    logger.debug('invoking a function in another module')
    gnlogger_test.some_function()

    logger.debug('creating an object from another module')
    obja = gnlogger_test.Auxiliary()
    logger.debug('infoking a function in created object')
    obja.do_something()


