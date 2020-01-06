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




## \namespace rdf.units.addendum Non metric and user units.
"""his modules instantiates units that do not fit the:

<prefix><metric>

format. Units are collected in to tuples of like dimension, however, that
is utterly unessesary, as the mere act of instaniation memoizes them
in the GLOSSARY

Users could add units here, or perhaps read them from an input file
"""
import operator
import math
from iscesys.Parsers.rdf.units.physical_quantity import *

dBPower('dB', 1)

## Supported _Length conversions
LENGTHS = (Length('in', 0.0254),
           Length('ft', 0.3048),
           Length('mi', 1.609344e3),
           Length('m/pixel', 1))

MASSES = (Mass('g', 0.001), )


## Supported _Area conversions
AREAS = (Area('mm*mm', 1e-6),
         Area('cm*cm', 1e-4),
         Area('km*km', 1e6),
         Area('in*in', 6.4516e-4),
         Area('ft*ft', 9.290304e-2),
         Area('mi*mi', 2.58995511e6))

## Supported _Time conversions
TIMES = (Time('min', 60),
         Time('hour', 3600),
         Time('day', 86400),
         Time('sec', 1),
         Time('microsec', 1e-6))


## Supported _Velocity conversions
VELOCITES = (Velocity('km/hr', operator.truediv(5, 18)),
             Velocity('ft/s', 0.3048),
             Velocity('mi/h', 0.44704))

POWERS = ()

## Supported dB Power
DBPOWERS = (dBPower('dBm', adder=-30),)

## Supported Frequency conversions
FREQUENCIES = (Frequency('rpm', operator.truediv(1,60)),
               Frequency('hz', 1),
               Frequency('Mhz', 1e6))

BYTES = (Byte('bytes', 1),)
PIXELS = (Pixel('pixels', 1),)

## Supported Angle conversions
ANGLES = (Angle('deg', operator.truediv(math.pi,180)),
          Angle('"', operator.truediv(math.pi, 180*3600)),
          Angle("'", operator.truediv(math.pi, 180*60)),
          Angle("arcsec", operator.truediv(math.pi, 180*3600)))

## Supported Temperature Conversions
TEMPERATURES = (Temperature('degK', 1.0, 273),
                Temperature('degF', operator.truediv(5, 9), -32.0))
#                Temperature('eV', 1.602176565e-19/1.3806488e-23))
                



