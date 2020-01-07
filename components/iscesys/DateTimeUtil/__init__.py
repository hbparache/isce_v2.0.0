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
# Author: Eric Belz
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



"""Date and Time utilites, on top of the datetime standard library.

New Usage:

>>>from iscesys import DateTimeUtil as DTU

replaces former usage:

>>>from iscesys.DateTimeUtil.DateTimeUtil import DateTimeUtil as DTU

Note, both:

javaStyleUtils()   and   pythonic_utils()

are available.
"""
from .DateTimeUtil import timedelta_to_seconds, seconds_since_midnight, date_time_to_decimal_year

## JavaStyleNames for the pythonic_names
timeDeltaToSeconds = timedelta_to_seconds
secondsSinceMidnight =  seconds_since_midnight
dateTimeToDecimalYear = date_time_to_decimal_year
