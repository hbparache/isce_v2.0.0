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




"""The nouns.NOUNS classes process Record or Comment lines. The class structure
may seem odd, and on it's own it is. It's structure is polymorphic to
the more complex Verb.VERB classes, which do much more.
"""
## \namespace rdf.language.lexis.semantics References to Things (Noun)
import abc
from iscesys.Parsers.rdf.language import lexis

class _Noun(lexis.Word):
    
    __metaclass__ = abc.ABCMeta
    
    def line_is(self, line, grammar):
        return (
            (grammar.operator in grammar.comment(line)[0]) ==
            self._operator_in_line
            )

    ## Calling a Verb lats the agent act on the patient.
    ## \param line A complete RDF sentence (str)
    ## \param grammar An rdf.language.grammar.syntax.Grammar instance
    ## \return Whatever the noun's concrete method returns
    def __call__(self, line, grammar):
        return self.concrete(line, grammar)

    ## Calling a noun makes it's concrete person place or thing from \n
    ## line, according to grammar
    ## \param line A complete RDF sentence (str)
    ## \param grammar An rdf.language.grammar.syntax.Grammar instance
    ## \return N/A: this is an <a href="http://docs.python.org/2/library/abc.html?highlight=abstractmethod#abc.abstractmethod">abstractmethod</a>
    @abc.abstractmethod
    def concrete(self, line, grammar):
        """Abstract method must be overriden in concrete subclasses"""

    ## W/o a concrete rep, you're not a noun.
    sin_qua_non = concrete


## The Record Noun processes the basic input: An RDF line.
class Record(_Noun):
    _operator_in_line = True
    ## act uses RDFField.__radd__ to build some form of an _RDFRecord \n
    ## (we don't know what that is here, no should we).
    @staticmethod
    def concrete(line, grammar):
        from iscesys.Parsers.rdf.language.grammar import punctuation
        from iscesys.Parsers.rdf.data.entries import RDFField
        left, comments = grammar.comment(line)
        left, value = grammar.operator(left)
        base_key, units, dimensions, element = punctuation.key_parse(left)
        return grammar.affix(base_key) + RDFField(value.strip(),
                                                  units=units,
                                                  dimensions=dimensions,
                                                  element=element,
                                                  comments=comments)

## The Comment Noun remembers passive comment lines.
class Comment(_Noun):
    _operator_in_line = False
    @staticmethod
    def concrete(line, grammar=NotImplemented):
        from iscesys.Parsers.rdf.data.entries import RDFComment
        line = line.strip()
        return RDFComment(line) if line else None # semi-Guard


## Nouns 
NOUNS = (Record, Comment)    
