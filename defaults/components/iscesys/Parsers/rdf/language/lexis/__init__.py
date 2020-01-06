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




## \namespace rdf.language.lexis The Lexis comprises the words in the language.
import abc

## The Pragamtic's are RDF lines meaning.
class Word(str):
    """Word is an ABC that subclasses str. It has a call
    that dyamically dispatches args = (line, grammar) to
    the sub classes' sin qua non method-- which is the
    method that allows them to do their business.
    """

    __metaclass__ = abc.ABCMeta

    # Call the Pragamtic's 'sin_qua_non' method -which is TBDD \n
    # (To be Dynamically Dispathed ;-)
    def __call__(self, line, grammar):
        return self.sin_qua_non(line, grammar)

    @abc.abstractmethod
    def sin_qua_non(self, line, grammar):
        pass
