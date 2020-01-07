#!/usr/bin/env python3

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2014 to the present, California Institute of Technology.
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
# Author: Eric Belz
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




"""Usage:

[python] ./parse.py src [dst]
"""

## \namespace rdf.parse RDF Parsing script
import sys
from rdf import rdfparse

# RUN AS AS SCRIPT
if __name__ == "__main__":

    # IF usage error, prepare error message and pipe->stderr, 
     #                set exit=INVALID INPUT
    if len(sys.argv) == 1: # guard
        import errno
        pipe = sys.stderr
        message = getattr(sys.modules[__name__], '__doc__')
        EXIT = errno.EINVAL
    # ELSE: Usage OK- the message is the result, and the pipe us stdout
    #                 set exit=0.
    else:
        argv = sys.argv[1:] if sys.argv[0].startswith('python') else sys.argv[:]
        src = argv[-1]
        pipe = sys.stdout
        message = str(rdfparse(src))
        EXIT = 0
        
    # Send message to pipe.
    print >> pipe, message
    # exit script
    sys.exit(EXIT)
# ELSE: I You cannot import this module b/c I say so.
else:
    raise ImportError("This is a script, and only a script")
