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




"""Brackets: This is where glyphs take on meaning"""
## \namespace rdf.language.grammar.punctuation Language's Punctuation Marks.

from __future__ import absolute_import

from iscesys.Parsers.rdf import reserved
from iscesys.Parsers.rdf.reserved import glyphs

## A symbol is a string that can split a line on it's left most occurance\n
## It's a puncuatin mark that can find itself
class Glyph(str):
    """A Glyph is a str sub-class that can be called.
    
    symbol(line) splits the line on the 1st occorence of symbol in
    line. If it is not in line, you still get 2 results:

    line, ""

    so it i basically an 2-ple safe unpacking of a split on self.
    """
    ## split line on self
    ## \param line A line
    ## \returns (left, right) side of line (with possible null str on right)
    def __call__(self, line):
        try:
            index = line.index(self)
        except ValueError:
            left, right = line, ""
        else:
            left = line[:index]
            right = line[index+1:]
        return map(str.strip, (left, right))
    
    ## Get line left of self
    ## \param line A line with or without self
    ## \retval left line left of self
    def left(self, line):
        """left symbol"""
        return self(line)[0]

    ## Get line right of self
    ## \param line A line with or without self
    ## \retval right line right of self
    def right(self, line):
        """right symbol"""
        return self(line)[-1]

    
## <a href="http://en.wikipedia.org/wiki/Bracket">Brackets</a> that
## know thy selves.
class Brackets(str):
    """_Delimeter('LR')

    get it? Knows how to find itself in line

    """
    ## L, R --> -, + \n + is right
    def __pos__(self):
        return self[-len(self)/2:]

    ## L, R --> -, + \n - is left
    def __neg__(self):
        return self[:len(self)/2]


    ## extract enclosed:  line<<pair
    # \param line An RDF sentence
    # \par Side Effects: 
    #  raises RDFWarning on bad grammar
    # \retval contents The string inside the Bracket
    def __rlshift__(self, line):
        """INPUTS: pair, line
    
        pair is 2 characters LR, this extracts part of line
        between L    and   R. Throws errors IF need be.
        """
        # 5 IF's are for error checking, not processing
        from iscesys.Parsers.rdf.language import errors
        ## Count start and stops
        count = map(line.count, self)
        ## Guard: early return.
        if min(count) is 0:   # Guard
            ## Check IF there is an oper/close error
            if max(count):   # Guard
                raise errors.UnmatchedBracketsError(self)
            return None
        ## Ensure 1 pair
        if max(count) > 1:   # Guard
            raise errors.RunOnSentenceError(self)
        i_start = line.index(-self) + 1
        i_stop = line.index(+self)
        ## ensure order:
        if i_stop <= i_start:    # Guard
            raise errors.BackwardBracketsError(self)
        contents = line[i_start : i_stop]
        # finally check for nonesense
        for single_char in contents:
            if single_char in reserved.RESERVED:   # Guard
                raise errors.ReservedCharacterError(self)
        return contents

    ## Insert: line>>pair or go blank
    def __rrshift__(self, line):
        """Insert non-zero line in string, or nothing"""
        return " %s%s%s " % (-self, str(line), +self) if line else ""
        
    __lshift__ = __rrshift__
    __rshift__ = __rlshift__
    
    ## (line in delimiter) IF the line has token in it legally
    # \param line an RDF sentence
    # \retval <bool> IF Bracket is in the line
    def __contains__(self, line):
        return ( (-self in line) and
                 (+self in line) and
                 line.index(-self) < line.index(+self) )

    ## line - delimiter removes delimeter from line, with no IF
    def __rsub__(self, line):
        """IF line in self __get_inner(line) else line"""
        return {True  : self.__get_inner,
                False : self.__no_inner}[line in self](line)
        
    ## Call IF line is in self, then go get it
    def __get_inner(self, line):
        return  (line[:line.index(-self)] +
                 line[1+line.index(+self):]).strip()
    
    ## Call IF line is not in self, a no-op.
    @staticmethod
    def __no_inner(line):
        return line
    
    
## Unit defining Brackets from rdf.reserved.glyphs.UNITS
UNITS =  Brackets(glyphs.UNITS)

## DIMENSIONS defining Brackets from rdf.reserved.glyphs.DIMENSIONS
DIMENSIONS = Brackets(glyphs.DIMENSIONS)

## ELEMENT defining Brackets from rdf.reserved.glyphs.ELEMENT
ELEMENT = Brackets(glyphs.ELEMENT)

## Tuple of RDF Optional Left Fields
_OPTIONAL_LEFT_FIELDS = (UNITS, DIMENSIONS, ELEMENT)


## Self explanatory
NUMBER_OF_OPTIONAL_LEFT_FIELDS = len(_OPTIONAL_LEFT_FIELDS)

## get ::_OPTIONAL_LEFT_FIELDS (olf).
def get_olf(left_line):
    """parse out UNITS DIMENSIONS ELEMENT from input line"""
    return [left_line << item for item in _OPTIONAL_LEFT_FIELDS]

## Get the key out of the left side of an rdf record \n
## Note: this relies on the Brackets.__rsub__ operator
def get_key(leftline):
    """Get key part only form a record line's left-of-operator portion"""
    return (leftline - UNITS - DIMENSIONS - ELEMENT).strip()

## get key and delimeters - the entrie left side of an rdf record, parsed
def key_parse(leftline):
    """Break left-of-operator portion into key, units, dimensions, element"""
    return [get_key(leftline)] + get_olf(leftline)



