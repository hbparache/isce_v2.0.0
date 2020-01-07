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


class grass(Component):
    '''Specific Connector from an insarApp object to a Grass object.''' 
    def __init__(self, obj):

        basename = obj.insar.topophaseFlatFilename
        self.wrapName = basename
        self.unwrapName = basename.replace('.flat', '.unw')

        ###To deal with missing filt_*.cor
        if basename.startswith('filt_'):
            self.corName  = basename.replace('.flat', '.cor')[5:]
        else:
            self.corName  = basename.replace('.flat', '.cor')
   
            self.width = obj.insar.resampIntImage.width

#   print("Wrap: ", self.wrapName)
#   print("Unwrap: ", self.unwrapName)
#   print("Coh: ", self.corName)
#   print("Width: ", self.width)


    def unwrap(self):
   
        with isceobj.contextIntImage(
            filename=self.wrapName,
            width=self.width,
            accessMode='read') as intImage:

            with isceobj.contextOffsetImage(
                filename=self.corName,
                width = self.width,
                accessMode='read') as cohImage:


                with isceobj.contextIntImage(
                    filename=self.unwrapName,
                    width = self.width,
                    accessMode='write') as unwImage:

                    grs=Grass()
                    grs.wireInputPort(name='interferogram',
                        object=intImage)
                    grs.wireInputPort(name='correlation',
                        object=cohImage)
                    grs.wireOutputPort(name='unwrapped interferogram',
                        object=unwImage)
                    grs.unwrap()
                    unwImage.renderHdr()

                    pass
                pass
            pass
    
        return None
