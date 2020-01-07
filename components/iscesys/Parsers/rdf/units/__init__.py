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




"""The unit module.

The rdf.data.entries.RDFField.__new__ only needs access to the
SI function-- which identifies units and converts them to nominal
inputs.

See SI.__doc__ on how Units are used.

"""
## \namespace rdf.units RDF units as spec'd
from iscesys.Parsers.rdf.units.physical_quantity import Unit
from iscesys.Parsers.rdf.units import addendum
from iscesys.Parsers.rdf.language import errors

## The global unit glossary dictionary:[symbol]->converter function
GLOSSARY = Unit.Glossary

## Convert (value, units) to SI pair - this is the interface to RDField
## Search various places for units...(TBD).
## \param value A float in units
## \param units a string describing the units
## \retval (converter(value),converter.si_unit) The new value in the right units
def SI(value, units):
    """
    Using Units:
    Unit instance are instance of <str>-- hence you can compare them or use them
    as keys in a dictionary. Hence:

    >>>km = physical_quantity.Length('km', 1000)
    
    is a string == 'km', and it is a function that multiplies by 1000.
    
    Thus: SI just looks in a dictionary of UNITS, c.f:
    
    {km : km}['km']
    
    which returns km, such that:
    
    >>>print km(1)
    1000.
    
    Sweet.
    
    See physical_quanity on how to make your own units and how to put them in
    the GLOASSRY.
    """
    try:
        converter = GLOSSARY[units]
    except KeyError:
        try:
            converter = runtime_units()[units]
        except KeyError:
            # raise errors.FatalUnitError to stop.
            raise errors.UnknownUnitWarning
    return converter(value), converter.si_unit



## A function to read user defined units at runtime (after import-- otherwise
## it's cyclic)-- format is provisional.
def runtime_units(src='units.rdf'):
    """read units from units.rdf:

    mym (m) {length} = 10000 ! A Myriameters is 10 K
    """
    from iscesys.Parsers.rdf import RDF
    try:
        result = RDF.fromfile(src)
    except IOError:
        result = {}
    return result
