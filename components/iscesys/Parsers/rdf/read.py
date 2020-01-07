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




## \namespace rdf.read Reading Functions
"""(Lazy) Functions to read rdf files and yield unwrapped lines"""

from __future__ import absolute_import

import itertools

from . import utils
from .reserved import glyphs

## unwrap lines from a generator
# \param gline A iteratable that pops file lines (rdf.utils.read_file())
# \param wrap = rdf.reserved.glyphs.WRAP The line coninutation character
# \retval< <a href="https://wiki.python.org/moin/Generators">Generator</a> 
# that generates complete RDF input lines. 
def _unwrap_lines(gline, wrap=glyphs.WRAP):
    """given a read_stream() generator, yield UNWRAPPED RDF lines"""
    while True:
        line = next(gline)
        while line.endswith(wrap):
            line = line[:-len(wrap)] + next(gline)
        yield line

## file name --> unwrapped lines
# \param src A file name
# \param wrap = rdf.reserved.glyphs.WRAP The line coninutation character
# \retval< <a href="https://wiki.python.org/moin/Generators">Generator</a> 
# that generates complete RDF input lines. 
def unwrap_file(src, wrap=glyphs.WRAP):
    """Take a file name (src) and yield unwrapped lines"""
    return itertools.ifilter(
        bool,
        _unwrap_lines(utils.read_file(src), wrap=wrap)
        )

