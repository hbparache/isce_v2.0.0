#!/usr/bin/env python3 

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
# Authors: Giangi Sacco, Eric Belz
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



"""Docstring"""

Version = "$Revision: 876$"
# $Source$ 
from iscesys.Compatibility import Compatibility
from isceobj.Planet.Planet import Planet
from isceobj.Planet.AstronomicalHandbook import c as SPEED_OF_LIGHT

EARTH = Planet('Earth')
EarthGM = EARTH.GM
EarthSpinRate = EARTH.spin
EarthMajorSemiAxis = EARTH.ellipsoid.a
EarthEccentricitySquared = EARTH.ellipsoid.e2

def nu2lambda(nu):
    return SPEED_OF_LIGHT/nu

def lambda2nu(lambda_):
    return SPEED_OF_LIGHT/lambda_
