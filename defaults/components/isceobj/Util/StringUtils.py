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
# Author: Eric Gurrola
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




from __future__ import print_function
from iscesys.Compatibility import Compatibility
Compatibility.checkPythonVersion()


class StringUtils(object):

    @staticmethod
    def lower_no_spaces(s):
        return (''.join(s.split())).lower()

    @staticmethod
    def lower_single_spaced(s):
        return (' '.join(s.split())).lower()

    @staticmethod
    def capitalize_single_spaced(s):
        return ' '.join(map(str.capitalize, s.lower().split()))

    @staticmethod
    def listify(a):
        """
        Convert a string version of a list, tuple, or comma-/space-separated
        string into a Python list of strings.
        """
        if not isinstance(a, str):
            return a

        if '[' in a:
            a = a.split('[')[1].split(']')[0]
        elif '(' in a:
            a = a.split('(')[1].split(')')[0]

        #At this point a is a string of one item or several items separated by
        #commas or spaces. This is converted to a list of one or more items
        #with any leading or trailing spaces stripped off.
        if ',' in a:
            return map(str.strip, a.split(','))
        else:
            return map(str.strip, a.split())

