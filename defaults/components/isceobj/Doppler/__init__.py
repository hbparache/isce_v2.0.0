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
# Authors: Walter Szeliga, Eric Gurrola
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



from __future__ import print_function

__all__ = ('createDoppler',)

def useDefault(name=None):
    if name:
        instance = None
    else:
        import isceobj.Doppler.DefaultDopp
        instance = DefaultDopp.DefaultDopp()
        return instance

def useDOPIQ(name=None):
    if name:
        instance = None
    else:
        import mroipac.dopiq.DopIQ
        instance = mroipac.dopiq.DopIQ.DopIQ()
        return instance

def useCalcDop(name=None):
    if name:
        instance = None
    else:
        import isceobj.Doppler.Calc_dop
        instance = isceobj.Doppler.Calc_dop.Calc_dop()
    return instance

def useDopTsx(name=None):
    if name:
        instance = None
    else:
        import isceobj.Doppler.TsxDopp
        instance = isceobj.Doppler.TsxDopp.TsxDopp()
    return instance

def useDopCskSlc(name=None):
    if name:
        instance = None
    else:
        import isceobj.Doppler.CskSlcDopp
        instance = isceobj.Doppler.CskSlcDopp.CskSlcDopp()
    return instance

def useDoppler(name=None):
    if name:
        instance = None
    else:
        import mroipac.doppler.Doppler
        instance = mroipac.doppler.Doppler.Doppler()
    return instance
    

doppler_facilities = {'USEDOPIQ' : useDOPIQ,
         'USECALCDOP' : useCalcDop,
         'USEDOPPLER' : useDoppler,
         'USEDOPTSX' : useDopTsx,
         'USEDOPCSKSLC' : useDopCskSlc,
         'USEDEFAULT': useDefault}


def createDoppler(doppler=None, name=None):
    if doppler.upper() in doppler_facilities.keys():
        instance = doppler_facilities[doppler.upper()](name)
    else:
        instance = None
        print(
            "Doppler calculation method not recognized. Valid methods: ",
            doppler_facilities.keys())
    return instance

