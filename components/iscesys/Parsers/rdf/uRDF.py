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




"""uRDF is the user's interface to rdf.

rdf_include  is the key function- it reads rdf files recursivly.

rdf_reader unpacks the result into the RDF constructor.
"""
## \namespace rdf.uRDF __u__ sers' inteface to language.py and data.py

from __future__ import absolute_import

from . import read
from .language.grammar import syntax
from .data.files import RDF
 

## The rdf_include function takes a src and rdf.language.syntax.Grammar 
## object to go process the entirety of src-- it is the sole controller 
## of Grammar.depth, unpacking of _RDFRecord and lists of them- it deals
## with the recursion, etc
## \param src Is the source file name
## \par Side Effect: None to external users (Grammar evolution internally)
## \retval< <a href="https://wiki.python.org/moin/Generators">Generator</a> 
## that generates rdf.data.entries.RDFRecord 
def rdf_include(src, **_kwargs):
    """rdf_include(src):

    src is an rdf file name. A generator is returned, and it yields
    RDFRecord objects one at time, in the order they come up.
    """
    # There is one keyword allowed, and it is secret
    # Get grammar passed in, or make a new one.
    _grammar = _kwargs.get('_grammar') or syntax.Grammar()

    # prepare grammar depth, or add on a recursive call
    _grammar += 1
    # read (full) line from src
    for line in read.unwrap_file(src, wrap=_grammar.wrap):
        # get the result as _grammar processes it.
        result = _grammar(line)
        # Polymorphic unpack:
        # RdfPreRecord -> RDFRecord
        # RDFComment --> [] --> break inner loop
        # () from commands  --> ditto
        # INCLUDE --> a bunch of records
        for item in result:
            yield item
    # to get here, you hit EOF, so you're moving up a level, or out for ever.
    _grammar -= 1


## For src it's that simple
## \param src Is the source file name
## \retval rdf.data.files.RDF The RDF mapping object
def rdf_reader(src):
    """rdf = rdf_reader(src)
    
    src      rdf filename
    rdf      The RDF mapping object"""
    return RDF(*rdf_include(src))


