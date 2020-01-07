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
# Author: Brett George
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



import logging
import isceobj.Catalog
import os
logger = logging.getLogger('isce._isce.createDem')

def createDem(self, info):
    #we get there only if a dem image was not specified as input
    import math
    from contrib.demUtils.DemStitcher import DemStitcher
    #import pdb
    #pdb.set_trace()
    bbox = info.bbox

    ####If the user has requested a bounding box
    if self.geocode_bbox:
        latMax = self.geocode_bbox[1]
        latMin = self.geocode_bbox[0]
        lonMin = self.geocode_bbox[3]
        lonMax = self.geocode_bbox[2]
    else:
        latMax = -1000
        latMin = 1000
        lonMax = -1000
        lonMin = 1000


    for bb in bbox:
        if bb[0] > latMax:
            latMax = bb[0]
        if bb[0] < latMin:
            latMin = bb[0]
        if bb[1] > lonMax:
            lonMax = bb[1]
        if bb[1] < lonMin:
            lonMin = bb[1]
    latMin = math.floor(latMin)
    latMax = math.ceil(latMax)
    lonMin = math.floor(lonMin)
    lonMax = math.ceil(lonMax)
    demName = self.demStitcher.defaultName([latMin,latMax,lonMin,lonMax])
    demNameXml = demName + '.xml'
    self.demStitcher.setCreateXmlMetadata(True)
    self.demStitcher.setMetadataFilename(demNameXml)#it adds the .xml automatically

    #if it's already there don't recreate it
    if not (os.path.exists(demNameXml) and os.path.exists(demName)):

        #check whether the user want to just use high res dems and filling the
        # gap or go to the lower res if it cannot complete the region
        # Better way would be to use the union of the dems and doing some
        # resampling
        if self.useHighResolutionDemOnly:
            #it will use the high res no matter how many are missing
            self.demStitcher.setFilling()
            #try first the best resolution
            source = 1
            stitchOk = self.demStitcher.stitchDems([latMin, latMax],
                                     [lonMin, lonMax],
                                     source,
                                     demName,
                                     keep=False)#remove zip files
        else:
            #try first the best resolution
            self.demStitcher.setNoFilling()
            source = 1
            stitchOk = self.demStitcher.stitchDems([latMin, latMax],
                                     [lonMin, lonMax],
                                     source,
                                     demName,
                                     keep=False)#remove zip files
            if not stitchOk:#try lower resolution if there are no data
                self.demStitcher.setFilling()
                source = 3
                stitchOk = self.demStitcher.stitchDems([latMin, latMax], [lonMin, lonMax],
                                         source, demName, keep=False)

        if not stitchOk:
            logger.error("Cannot form the DEM for the region of interest. If you have one, set the appropriate DEM component in the input file.")
            raise Exception

    #save the name just in case
    self._isce.demInitFile = demNameXml
    #if stitching is performed a DEM image instance is created (returns None otherwise). If not we have to create one
    demImage = self.demStitcher.getImage()
    if demImage is None:
        from iscesys.Parsers.FileParserFactory import createFileParser
        from isceobj import createDemImage
        parser = createFileParser('xml')
        #get the properties from the file init file
        prop, fac, misc = parser.parse(demNameXml)
        #this dictionary has an initial dummy key whose value is the dictionary with all the properties

        demImage  = createDemImage()
        demImage.init(prop,fac,misc)

    self._isce.demImage = demImage

    # when returning from here an image has been created and set into
    # self_.insar
