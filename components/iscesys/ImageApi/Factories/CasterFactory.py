#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2010 to the present, California Institute of Technology.
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
# Author: Giangi Sacco
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



from __future__ import print_function
import sys
import math
import logging

dataTypesReal = ['BYTE','CHAR','SHORT','INT','LONG','FLOAT','DOUBLE']
dataTypesCpx = ['CBYTE','CCHAR','CSHORT','CINT','CLONG','CFLOAT','CDOUBLE']


def getCaster(datain,dataout):
    suffix = 'Caster'
    if(datain.upper() in dataTypesReal and dataout.upper() in  dataTypesReal):
        typein = datain.lower().capitalize()
        typeout = dataout.lower().capitalize()
    elif(datain.upper() in dataTypesCpx and dataout.upper() in dataTypesCpx):
        typein = datain[1:].lower().capitalize()
        typeout = dataout[1:].lower().capitalize()
        suffix = 'CpxCaster'
    else:
        print('Casting only allowed between compatible types and not',datain,'and',dataout)  
        raise ValueError
    if typein == typeout:
        caster = ''
    else:
        caster = typein + 'To' + typeout + suffix
    return caster
