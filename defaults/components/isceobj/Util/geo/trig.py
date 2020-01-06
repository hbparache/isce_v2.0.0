#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2012 to the present, California Institute of Technology.
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



"""A place to store trig functions using degrees-- so if you don't have numpy
you can use math-- but just have numpy

"""
## \namespace geo.trig Trig functions in degrees


import numpy as np

## cosine in degress (math could be <a href="http://numpy.scipy.org/">numpy</a>
cosd = lambda x: np.cos(np.radians(x))
## sine in degrees
sind = lambda x: np.sin(np.radians(x))
## tangent, in degrees
tand = lambda x: np.tan(np.radians(x))
## arc tan in degrees (2 arg)
arctand2 = lambda y, x: np.degrees(np.arctan2(y, x))
## arc tan in degrees (1 arg)
arctand = lambda x: np.degrees(np.arctan(x)) 


