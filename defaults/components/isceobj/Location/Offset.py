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
# Author: Walter Szeliga
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




import math
import os
import logging
import logging.config
logging.config.fileConfig(os.path.join(os.environ['ISCE_HOME'], 'defaults',
    'logging', 'logging.conf'))

from isceobj.Util.decorators import type_check, force, pickled, logged

@pickled
class Offset(object):
    """A class to represent the two-dimensional offset of a particular
    location"""

    logging_name = "isceobj.Location.Offset"

    @logged
    def __init__(self, x=None, y=None, dx=None, dy=None, snr=0.0, sigmax=0.0, sigmay=0.0, sigmaxy=0.0):
        self.x = x
        self.dx = dx
        self.y = y
        self.dy = dy
        self.setSignalToNoise(snr)
        self.setCovariance(sigmax, sigmay, sigmaxy)
        return None

    def setCoordinate(self, x, y):
        self.x = x
        self.y = y

    def setOffset(self, dx, dy):
        self.dx = dx
        self.dy = dy
        pass
    def setCovariance(self, covx, covy, covxy):
        self.sigmax = covx
        self.sigmay = covy
        self.sigmaxy = covxy

    @force(float)
    def setSignalToNoise(self, snr):
        self.snr = snr if not math.isnan(snr) else 0.0

    def getCoordinate(self):
        return self.x,self.y

    def getOffset(self):
        return self.dx,self.dy

    def getSignalToNoise(self):
        return self.snr

    def getCovariance(self):
        return self.sigmax, self.sigmay, self.sigmaxy

    def __str__(self):
        retstr = "%s %s %s %s %s %s %s %s" % (self.x,self.dx,self.y,self.dy,self.snr, self.sigmax, self.sigmay, self.sigmaxy)
        return retstr

@pickled
class OffsetField(object):
    """A class to represent a collection of offsets defining an offset field"""
    logging_name = "isceobj.Location.OffsetField"

    @logged
    def __init__(self):
        self._last = 0
        self._offsets = []
        return None

    def getLocationRanges(self):
        xdxydysnr = self.unpackOffsets()
        numEl = len(xdxydysnr)
        x = np.zeros(numEl)
        y = np.zeros(numEl)
        for i in range(numEl):
            x[i] =  xdxydysnr[i][0]
            y[i] =  xdxydysnr[i][2]
        xr = sorted(x)
        yr = sorted(y)
        return [xr[0],xr[-1],yr[0],yr[-1]]

    def plot(self,type,xmin = None, xmax = None, ymin = None, ymax = None):
        try:
            import numpy as np
            from  scipy.interpolate import griddata
            import matplotlib.pyplot as plt
            from pylab import quiver,quiverkey
        except ImportError:
            self.logger.error('This method requires scipy, numpy and matplotlib to be installed.')
        xdxydysnr = self.unpackOffsets()
        numEl = len(xdxydysnr)
        x = np.zeros(numEl)
        y = np.zeros(numEl)
        dx = np.zeros(numEl)
        dy = np.zeros(numEl)
        for i in range(numEl):
            x[i] =  xdxydysnr[i][0]
            dx[i] =  xdxydysnr[i][1]
            y[i] =  xdxydysnr[i][2]
            dy[i] =  xdxydysnr[i][3]
        if xmin is None: xmin = np.min(x)
        if xmax is None: xmax = np.max(x)
        if ymin is None: ymin = np.min(y)
        if ymax is None: ymax = np.max(y)
        legendL = np.floor(max(np.max(dx),np.max(dy)))
        #normally the width in range is much smaller that the length in azimuth, so normalize so that we have the same number os sample for each axis
        step = min(np.min(int(np.ceil(((ymax - ymin)/(xmax - xmin))))),5)
        X , Y = np.mgrid[xmin:xmax,ymin:ymax:step]
        skip = int(np.ceil(xmax - xmin)/100)*5
        if type == 'field':
            U = griddata(np.array([x,y]).T,dx, (X,Y), method='linear')
            V = griddata(np.array([x,y]).T,dy, (X,Y), method='linear')
            Q = quiver(X[::skip,::skip], Y[::skip,::skip],
                       U[::skip,::skip], V[::skip,::skip],
                       pivot='mid', color='g')
            arrow = str(legendL) + ' pixles'
            qk = quiverkey(Q, 0.8, 0.95, legendL, arrow,
                           labelpos='E',
                           coordinates='figure',
                           fontproperties={'weight':'bold'})
            ax = Q.axes
            ax.set_xlabel('range location')
            ax.set_ylabel('azimuth location')
        elif(type == 'pcolor'):
            M = griddata(np.array([x,y]).T,
                         np.sqrt(dx**2 + dy**2),
                         (X,Y),
                         method='linear')
            P = griddata(np.array([x,y]).T,
                         np.arctan2(dy, dx),
                         (X,Y)
                         ,method='linear')
            plt.subplot(2, 1, 1)
            plt.imshow(M,aspect='auto', extent=[xmin, xmax, ymin, ymax])
            plt.colorbar()
            ax1 = plt.gca()
            ax1.set_ylabel('azimuth location')
            ax1.set_title('offset magnitude')
            plt.subplot(2, 1, 2)
            plt.imshow(P, aspect='auto', extent=[xmin,xmax,ymin,ymax])
            plt.colorbar()
            ax2 = plt.gca()
            ax2.set_xlabel('range location')
            ax2.set_ylabel('azimuth location')
            ax2.set_title('offset phase')
        plt.show()
        return plt

    @type_check(Offset)
    def addOffset(self, offset):
        self._offsets.append(offset)
        pass

    def __next__(self):
        if self._last < len(self._offsets):
            next = self._offsets[self._last]
            self._last += 1
            return next
        else:
            self._last = 0 # This is so that we can restart iteration
            raise StopIteration()

    def packOffsets(self, offsets):#crete an offset field from a list of offets
        for i in range(len(offsets[0])):
            #note that different ordering (x,y,dx,dy,snr) instead of (x,dx,y,dy,snr)
            self.addOffset(
                Offset(offsets[0][i],
                       offsets[2][i],
                       offsets[1][i],
                       offsets[3][i],
                       offsets[4][i])
                )

    def packOffsetswithCovariance(self, offsets):
        for i in range(len(offsets[0])):
            self.addOffset(
                    Offset(offsets[0][i],
                           offsets[2][i],
                           offsets[1][i],
                           offsets[3][i],
                           offsets[4][i],
                           offsets[5][i],
                           offsets[6][i],
                           offsets[7][i])
                    )

    def unpackOffsets(self):
        """A convenience method for converting our iterator into a flat
        list for use in Fortran and C code"""
        offsetArray = []
        for offset in self.offsets:
            x, y = offset.getCoordinate()
            dx, dy = offset.getOffset()
            snr = offset.getSignalToNoise()
            offsetArray.append([x,dx,y,dy,snr])
            pass
        return offsetArray

    def unpackOffsetswithCovariance(self):
        offsetArray = []
        for offset in self.offsets:
            x,y = offset.getCoordinate()
            dx,dy = offset.getOffset()
            snr = offset.getSignalToNoise()
            sx, sy, sxy = offset.getCovariance()
            offsetArray.append([x,dx,y,dy,snr,sx,sy,sxy])
            pass
        return offsetArray

    def cull(self, snr=0.0):
        """Cull outliers based on their signal-to-noise ratio.

        @param snr: the signal-to-noise ratio to use in the culling.  Values with greater signal-to-noise will be kept.
        """
        culledOffsetField = OffsetField()
        i = 0
        for offset in self.offsets:
            if (offset.getSignalToNoise() < snr):
                i += 1
            else:
                culledOffsetField.addOffset(offset)

        self.logger.info("%s offsets culled" % (i))
        return culledOffsetField

    def __iter__(self):
        return self

    def __str__(self):
        return '\n'.join(map(str, self.offsets))+'\n' #2013-06-03 Kosal: wrong use of map

    @property
    def offsets(self):
        return self._offsets

    pass
