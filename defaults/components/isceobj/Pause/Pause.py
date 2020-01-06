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




from __future__ import print_function
from iscesys.Compatibility import Compatibility
Compatibility.checkPythonVersion()


class Pause(object):
    """
Pause: a class with method 'pause' to pause processing until the continueString is entered.\n
constructor is Pause(continueString=val, ignorePause=val, exitString=val) with defaults\n
continueString='continue', ignorePause=False, exitString=exit if no arguments are given to the\n
constructor.  These arguments to the constructor can be passed as positional arguments\n
in the order given above.
    """
    
    def __init__(self,continueString="continue",ignorePause=False, exitString="exit"):
        self.continueString = continueString
        self.ignorePause = ignorePause
        self.exitString = exitString
        return
    
        
    def pause(self):
        if self.ignorePause:
            return

        x = ""
        while x != self.continueString:
            x = raw_input()
            if x == self.exitString:
                import sys
                sys.exit(1)

        return


raise DepreacationWaring("use the Pause.pause module function.")
