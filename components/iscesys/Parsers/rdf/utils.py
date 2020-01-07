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




"""Non RDF specific python helpers"""
## \namespace rdf.utils Non-RDF specific utilities

## Generate non-zero entries from an ASCII file
## \param src Is the source file name
## \param purge = True reject blanks (unless False)
## \retval< <a href="https://wiki.python.org/moin/Generators">Generator</a> 
## that generates (nonzero) lines for an ASCII file
def read_file(src):
    """src --> src file name
    purge=True igonors black lines"""
    with open(src, 'r') as fsrc:
        for line in read_stream(fsrc):
            yield line

## Yield stripped lines from a file
## \param fsrc A readable file-like object
## \retval< <a href="https://wiki.python.org/moin/Generators">Generator</a> 
## that generates fsrc.readline() (stripped).
def read_stream(fsrc):
    """Generate lines from a stream (fsrc)"""
    tell = fsrc.tell()
    line = fsrc.readline().strip()
    while tell != fsrc.tell() or line:
        yield line
        tell = fsrc.tell()
        line = fsrc.readline().strip()

