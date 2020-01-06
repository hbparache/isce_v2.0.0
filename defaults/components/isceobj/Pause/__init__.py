#!/usr/bin/env python3

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2012 to the present, California Institute of Technology.
# ALL RIGHTS RESERVED. United States Government Sponsorship acknowledged.
# Any commercial use must be negotiated with the Office of Technology Transfer
# at the California Institute of Technology.
# 
# This software may be subject to U.S. export control laws. By accepting this
# software, the user agrees to comply with all applicable U.S. export laws and
# regulations. User has the responsibility to obtain export licenses,  or other
# export authority as may be required before exporting such information to
# foreign countries or providing access to foreign persons.
# 
# Installation and use of this software is restricted by a license agreement
# between the licensee and the California Institute of Technology. It is the
# User's responsibility to abide by the terms of the license agreement.
#
# Author: Eric Gurrola
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




## pause is a raw_input wrapper
def pause(cont="go",ex="exit",ignore=False, message="", bell=True):
    """pause function.  Pauses execution awaiting input.
    Takes up to three optional arguments to set the action strings:
    cont   = first positional or named arg whose value is a string that causes execution
              to continue.
              Default cont="go"
    ex     = second positional or named arg whose value is a string that causes execution
              to stop.
              Default ex="exit"
    ignore = third positional or named arg whose value cause the pause to be ignored or
              paid attention to.
              Default False
    message = and optional one-time message to send to the user"
    bell    = True: ring the bell when pause is reached.
    """
    if not ignore:
        x = ""
        if message or bell:
            message += chr(7)*bell
            print(message)
        while x != cont:
            try:
                x = raw_input(
                    "Type %s to continue; %s to exit: " % (cont, ex)
                    )
            except KeyboardInterrupt:
                return None
            if x == ex:
                # return the "INTERUPT" system error.
                import errno
                import sys
                return sys.exit(errno.EINTR)
            pass
        pass
    return None
