#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2013 to the present, California Institute of Technology.
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
# Author: Piyush Agram
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



from __future__ import print_function
import os
from . import snaphu
from . import grass
from . import icu
from . import snaphu_mcf

Unwrappers = {'SNAPHU' : snaphu.snaphu,
              'GRASS'  : grass.grass,
              'ICU'    : icu.icu,
              'SNAPHU_MCF' : snaphu_mcf.snaphu_mcf}


def createUnwrapper(unwrap, unwrapper_name, name=None):
    '''Implements the logic between unwrap and unwrapper_name to choose the unwrapping method.'''
    unwMethod = None

#    print('Unwrap = ', unwrap)
#    print('Unwrapper Name = ', unwrapper_name)

    #If no unwrapping name is provided.
    if (unwrapper_name is None) or (unwrapper_name is ''):
    #But unwrapped results are desired, set to default: grass
        if unwrap is True:
            unwMethod = 'grass'

    #Unwrap should be set to true.
    elif unwrap is True:
        unwMethod = unwrapper_name

#    print('Algorithm: ', unwMethod)

    if unwMethod is not None:
        try:
            cls = Unwrappers[str(unwMethod).upper()]
            print(cls.__module__)
        except AttributeError:
            raise TypeError("'unwrapper type'=%s cannot be interpreted"%
                            str(unwMethod))
            pass

    else:
        cls = None

    return cls
