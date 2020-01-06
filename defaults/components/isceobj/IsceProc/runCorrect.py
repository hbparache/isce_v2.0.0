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
# Author: Kosal Khun
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# Comment: Adapted from InsarProc/runCorrect.py
import logging

import isceobj
import stdproc
from iscesys.ImageUtil.ImageUtil import ImageUtil as IU
import os

logger = logging.getLogger('isce.isce.runCorrect') 


def runCorrect(self):
    refScene = self._isce.refScene
    velocity, height = self._isce.vh()

    infos = {}
    for attribute in ['dopplerCentroid', 'peg', 'lookSide', 'numberRangeLooks', 'numberAzimuthLooks', 'topophaseMphFilename', 'topophaseFlatFilename', 'heightSchFilename', 'is_mocomp']:
        infos[attribute] = getattr(self._isce, attribute)

    infos['refOutputPath'] = os.path.join(self.getoutputdir(refScene), refScene)
    stdWriter = self._stdWriter

    for sceneid1, sceneid2 in self._isce.selectedPairs:
        pair = (sceneid1, sceneid2)
        objMocompbaseline = self._isce.mocompBaselines[pair]
        for pol in self._isce.selectedPols:
            frame1 = self._isce.frames[sceneid1][pol]
            objFormSLC1 = self._isce.formSLCs[sceneid1][pol]
            topoIntImage = self._isce.topoIntImages[pair][pol]
            sid = self._isce.formatname(pair, pol)
            infos['outputPath'] = os.path.join(self.getoutputdir(sceneid1, sceneid2), sid)           
            catalog = isceobj.Catalog.createCatalog(self._isce.procDoc.name)
            run(frame1, objFormSLC1, objMocompbaseline, topoIntImage, velocity, height, infos, stdWriter, catalog=catalog, sceneid=sid)



def run(frame1, objFormSLC1, objMocompbaseline, topoIntImage, velocity, height, infos, stdWriter, catalog=None, sceneid='NO_ID'):
    logger.info("Running correct: %s" % sceneid)


    intImage = isceobj.createIntImage()
    #just pass the image object to Correct and it will handle the creation
    # and deletion of the actual image pointer  
    IU.copyAttributes(topoIntImage, intImage)

    posIndx = 1
    mocompPosition1 = objFormSLC1.mocompPosition

    centroid = infos['dopplerCentroid'].getDopplerCoefficients(inHz=False)[0]

    planet = frame1.instrument.platform.planet
    prf1 = frame1.instrument.PRF

    objCorrect = stdproc.createCorrect()
    objCorrect.wireInputPort(name='peg', object=infos['peg'])
    objCorrect.wireInputPort(name='frame', object=frame1)
    objCorrect.wireInputPort(name='planet', object=planet)
    objCorrect.wireInputPort(name='interferogram', object=intImage)
    objCorrect.wireInputPort(name='masterslc', object=objFormSLC1) #Piyush
    objCorrect.setDopplerCentroidConstantTerm(centroid)
    # Average velocity and height measurements       
    objCorrect.setBodyFixedVelocity(velocity)
    objCorrect.setSpacecraftHeight(height)
    # Need the reference orbit from Formslc       
    objCorrect.setReferenceOrbit(mocompPosition1[posIndx]) 
    objCorrect.setMocompBaseline(objMocompbaseline.baseline) 
    sch12 = objMocompbaseline.getSchs()
    objCorrect.setSch1(sch12[0])
    objCorrect.setSch2(sch12[1])
    sc = objMocompbaseline.sc
    objCorrect.setSc(sc)
    midpoint = objMocompbaseline.midpoint
    objCorrect.setMidpoint(midpoint)
    objCorrect.setLookSide(infos['lookSide'])

    objCorrect.setNumberRangeLooks(infos['numberRangeLooks'])
    objCorrect.setNumberAzimuthLooks(infos['numberAzimuthLooks'])
    objCorrect.setTopophaseMphFilename(infos['outputPath'] + '.' + infos['topophaseMphFilename'])
    objCorrect.setTopophaseFlatFilename(infos['outputPath'] + '.' + infos['topophaseFlatFilename'])
    objCorrect.setHeightSchFilename(infos['refOutputPath'] + '.' + infos['heightSchFilename'])

    objCorrect.setISMocomp(infos['is_mocomp'])
    #set the tag used in the outfile. each message is precided by this tag
    #is the writer is not of "file" type the call has no effect
    objCorrect.stdWriter = stdWriter.set_file_tags("correct",
                                                   "log",
                                                   "err",
                                                   "out")
    
    objCorrect()#.correct()

    if catalog is not None:
        # Record the inputs and outputs
        isceobj.Catalog.recordInputsAndOutputs(catalog, objCorrect,
                                               "runCorrect.%s" % sceneid,
                                               logger,
                                               "runCorrect.%s" % sceneid)

    return objCorrect
