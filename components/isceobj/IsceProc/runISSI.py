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
# Author: Kosal Khun
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# Comment: Adapted from contrib/ISSI/FR.py
import sys
import os
import math
from contrib.ISSI.FR import FR
from ISSI import Focuser
from make_raw import make_raw
from mroipac.geolocate.Geolocate import Geolocate

import logging
logger = logging.getLogger('isce.isceProc.runISSI')


def runISSI(self, opList):
    for sceneid in self._isce.selectedScenes:
        raws = {}
        slcFiles = {}
        for pol in ['hh', 'hv', 'vh', 'vv']:
            raws[pol] = make_raw()
            raws[pol].frame = self._isce.frames[sceneid][pol]
            slcFiles[pol] = self._isce.slcImages[sceneid][pol]
        focuser = Focuser(hh=raws['hh'], hv=raws['hv'], vh=raws['vh'], vv=raws['vv'])
        focuser.filter = self.FR_filter
        focuser.filterSize = (int(self.FR_filtersize_x), int(self.FR_filtersize_y))
        focuser.logger = logger

        outputs = {}
        for fname in [self._isce.frOutputName, self._isce.tecOutputName, self._isce.phaseOutputName]:
            outputs[fname] = os.path.join(self.getoutputdir(sceneid), self._isce.formatname(sceneid, ext=fname+'.slc'))

        hhFile = slcFiles['hh']
        issiobj = FR(hhFile=hhFile.filename,
                     hvFile=slcFiles['hv'].filename,
                     vhFile=slcFiles['vh'].filename,
                     vvFile=slcFiles['vv'].filename,
                     lines=hhFile.length,
                     samples=hhFile.width,
                     frOutput=outputs[self._isce.frOutputName],
                     tecOutput=outputs[self._isce.tecOutputName],
                     phaseOutput=outputs[self._isce.phaseOutputName])

        if 'polcal' in opList: ## polarimetric calibration
            issiobj.polarimetricCorrection(self._isce.transmit, self._isce.receive)
            for pol, fname in zip(['hh', 'hv', 'vh', 'vv'], [issiobj.hhFile, issiobj.hvFile, issiobj.vhFile, issiobj.vvFile]):
                self._isce.slcImages[sceneid][pol].filename = fname

        if 'fr' in opList: ## calculate faraday rotation
            frame = self._isce.frames[self._isce.refScene][self._isce.refPol]
            if frame.getImage().byteOrder != sys.byteorder[0]:
                logger.info("Will swap bytes")
                swap = True
            else:
                logger.info("Will not swap bytes")
                swap = False

            issiobj.calculateFaradayRotation(filter=focuser.filter, filterSize=focuser.filterSize, swap=swap)
            aveFr = issiobj.getAverageFaradayRotation()
            logger.info("Image Dimensions %s: %s x %s" % (sceneid, issiobj.samples,issiobj.lines))
            logger.info("Average Faraday Rotation %s: %s rad (%s deg)" % (sceneid, aveFr, math.degrees(aveFr)))

        if 'tec' in opList:
            date = focuser.hhObj.frame.getSensingStart()
            corners, lookAngles = focuser.calculateCorners()
            lookDirections = focuser.calculateLookDirections()
            fc = focuser.hhObj.frame.getInstrument().getRadarFrequency()
            meankdotb = issiobj.frToTEC(date, corners, lookAngles, lookDirections, fc)
            logger.info("Mean k.B value %s: %s" % (sceneid, meankdotb))

        if 'phase' in opList:
            fc = focuser.hhObj.frame.getInstrument().getRadarFrequency()
            issiobj.tecToPhase(fc)

