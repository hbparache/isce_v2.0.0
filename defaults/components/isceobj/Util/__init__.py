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




# next two functions are used to check two  strings are the same regardless of
# capitalization and/or white spaces and returns a dictionary value based on
# the string provided
def same_content(a,b):
     '''
     it seems an overkill
     al = a.lower().split()
     bl = b.lower().split()
     if len(al) == len(bl):
          for cl, cr in zip(al, bl):
               if cl != cr:
                    return False
          return True
     return False
     '''
     return True if(''.join(a.lower().split()) == ''.join(b.lower().split())) else False


def key_of_same_content(k,d):
     for kd in d:
         if same_content(k, kd):
             return kd, d[kd]
     raise KeyError("key %s not found in dictionary" % k)

def createCpxmag2rg():
    from .Cpxmag2rg import Cpxmag2rg
    return Cpxmag2rg()

def createOffoutliers():
    from .Offoutliers import Offoutliers
    return Offoutliers()

def createEstimateOffsets(name=''):
    from .EstimateOffsets import EstimateOffsets
    return EstimateOffsets(name=name)

def createDenseOffsets(name=''):
    from .DenseOffsets import DenseOffsets
    return DenseOffsets(name=name)

def createSimamplitude():
    from .Simamplitude import Simamplitude
    return Simamplitude()
