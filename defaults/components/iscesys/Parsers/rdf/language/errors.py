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




"""RDF Exceptions"""
## \namespace rdf.language.errors RDF Exceptions


## Fatal attempt to CODE badly
class RDFError(Exception):
    """Base RDF Error for BAD RDF coding (Fatal)"""
    
## <a href="http://en.wikipedia.org/wiki/Speech_error">Morphere Exchange
## Currents</a>?
class MorphemeExchangeError(RDFError):
    """fix-pre and/or sufix would cast list v. str type errors on "+" 
    anyway, so this is a TypeError
    """

class FatalUnitError(RDFError):
    """raise for unregocnized units (fatally)"""


## RDF Warning of INPUT problems
class RDFWarning(Warning):
    """Base RDF Warning for bad RDF input grammar"""
    
    
class UnknownUnitWarning(Warning):
    """Unrecognized unit (ignored)"""
    
    
## RDF Error for a unit problem (not sure what kind of error this is)
class UnitsError(RDFWarning, ValueError):
    """Raised for a non-existent unit"""

    
## Error for using a character in RESERVED
class ReservedCharacterError(RDFWarning):
    """Error for using a RESERVED character badly"""

    
## Unmatched or un parsable pairs
class UnmatchedBracketsError(ReservedCharacterError):
    """1/2 a delimeter was used"""

    
## Unmatched or un parsable pairs
class RunOnSentenceError(ReservedCharacterError):
    """Too many punctuation marks"""

    
## Unmatched or un parsable pairs
class BackwardBracketsError(ReservedCharacterError):
    """Inverted Punctuation"""

    
## Should be thrown in constructor?
class NullCommandError(RDFWarning):
    """Setting a required command to nothing"""


