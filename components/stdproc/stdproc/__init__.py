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



from .formslc import *
from .resamp import *
from .resamp_image import *
from .resamp_amps import *
from .resamp_only import *
from .resamp_slc import *
from .topo import *
from .correct import createCorrect, contextCorrect
from .mocompTSX import *
from .estamb import *

#ing added sensor argument to turn it into a real factory, allowing other type
# of formSLC and moved instantiation here
def createFormSLC(sensor=None, name=''):
    if sensor is None:
        from .formslc.Formslc import Formslc as cls
        return cls(name=name)
    elif str(sensor).lower() in ['terrasarx','cosmo_skymed_slc','radarsat2','sentinel1a','tandemx','kompsat5']:
        from .mocompTSX.MocompTSX import MocompTSX as cls
    else:
        raise ValueError("Unregocnized Sensor: %s" % str(sensor))
    return cls()




