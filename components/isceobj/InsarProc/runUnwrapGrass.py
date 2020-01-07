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




import sys
import isceobj
from iscesys.Component.Component import Component
from mroipac.grass.grass import Grass

# giangi: taken Piyush code grass.py and adapted

def runUnwrap(self):
    wrapName = self.insar.topophaseFlatFilename
    unwrapName = self.insar.unwrappedIntFilename
    corName = self.insar.coherenceFilename
    width = self.insar.resampIntImage.width
    with isceobj.contextIntImage(
        filename=wrapName,
        width=width,
        accessMode='read') as intImage:

        with isceobj.contextOffsetImage(
            filename=corName,
            width = width,
            accessMode='read') as cohImage:


            with isceobj.contextUnwImage(
                filename=unwrapName,
                width = width,
                accessMode='write') as unwImage:

                grs=Grass(name='insarapp_grass')
                grs.configure()
                grs.wireInputPort(name='interferogram',
                    object=intImage)
                grs.wireInputPort(name='correlation',
                    object=cohImage)
                grs.wireInputPort(name='unwrapped interferogram',
                    object=unwImage)
                grs.unwrap()
                unwImage.renderHdr()

                pass
            pass
        pass

    return None
