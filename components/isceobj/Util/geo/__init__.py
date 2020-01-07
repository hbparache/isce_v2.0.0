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



"""geo is for doing coordinates on Earth. Here are the modules:


euclid           Scalar, Vector, Tensor objects in E3 -eucliden 3-space.
charts           rotations in E3, aka: charts on SO(3).
affine           rigid affine transformations in E3.
coordinates      Coordinates on Earth
ellipsoid        oblate ellipsoid of revolution (e.g, WGS84) with all the
                 bells and whistles.


  Note: sub-package use __all__, so they are:
  >>>from geo import *
  safe.

  See mainpage.txt for a complete dump of geo's philosophy-- otherwise,
  use the docstrings.
"""
import os
isce_path  = os.getenv("ISCE_HOME")

## \namespace geo  Vector- and Affine-spaces, on Earth
__all__ = ['euclid', 'coordinates', 'ellipsoid', 'charts', 'affine', 'motion']


