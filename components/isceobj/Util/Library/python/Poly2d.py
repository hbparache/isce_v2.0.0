#!/usr/bin/env python

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



import numpy as np

class Polynomial(object):
    '''
    Class to store 2D polynomials in ISCE.
    Implented as a list of lists, the coefficients
    are stored as shown below:

    [ [    1,     x^1,     x^2, ....],
      [  y^1, x^1 y^1, x^2 y^1, ....],
      [  y^2, x^1 y^2, x^2 y^2, ....],
      [    :        :        :     :]]

    where "x" corresponds to pixel index in range and
    "y" corresponds to pixel index in azimuth.

    The size of the 2D matrix will correspond to
    [rangeOrder+1, azimuthOrder+1].
    '''

    def __init__(self, rangeOrder=None, azimuthOrder=None):
        '''
        Constructor for the polynomial object.
        '''
        self._coeffs = []

        if (azimuthOrder is not None) and (rangeOrder is not None):
            for k in range(azimuthOrder+1):
                rng =[]
                for kk in range(rangeOrder+1):
                    rng.append(0.)
                self._coeffs.append(rng)

            self._rangeOrder = int(rangeOrder)
            self._azimuthOrder = int(azimuthOrder)
        else:
            self._rangeOrder = None
            self._azimuthOrder = None
        self._normRange = 1.0
        self._normAzimuth = 1.0
        self._meanRange = 0.0
        self._meanAzimuth = 0.0

        return

    def setCoeffs(self, parms):
        '''
        Set the coefficients using another nested list.
        '''
        for ii,row in enumerate(parms):
            for jj,col in enumerate(row):
                self._coeffs[ii][jj] = float(col)

        return

    def setCoeff(self, ii, jj, val):
        self._coeffs[ii][jj] = float(val)

    def getCoeffs(self):
        return self._coeffs

    def getCoeff(self, ii, jj):
        return self._coeffs[ii][jj]

    def setNormRange(self, parm):
        self._normRange = float(parm)

    def setMeanRange(self, parm):
        self._meanRange = float(parm)

    def getNormRange(self):
        return self._normRange

    def getMeanRange(self):
        return self._meanRange

    def setNormAzimuth(self, parm):
        self._normAzimuth = float(parm)

    def setMeanAzimuth(self, parm):
        self._meanAzimuth = float(parm)

    def getNormAzimuth(self):
        return self._normAzimuth

    def getMeanAzimuth(self):
        return self._meanAzimuth

    def __call__(self, azi,rng):
        '''
        Evaluate the polynomial.
        This is much slower than the C implementation - only for sparse usage.
        '''
        y = (azi - self._meanAzimuth)/self._normAzimuth
        x = (rng - self._meanRange)/self._normRange
        res = 0.
        for ii,row in enumerate(self._coeffs):
            yfact = y**ii
            for jj,col in enumerate(row):
                res += col*yfact * (x**jj)

        return res

    def exportToC(self):
        '''
        Use the extension module and return a pointer in C.
        '''
        from isceobj.Util import combinedlibmodule as CL
        order = [self._azimuthOrder, self._rangeOrder]
        means = [self._meanAzimuth, self._meanRange]
        norms = [self._normAzimuth, self._normRange]
        ptr = CL.exportPoly2DToC(order, means, norms, self._coeffs)
        return ptr

    def importFromC(self, pointer, clean=True):
        '''
        Uses information from the  extension module structure to create Python object.
        '''
        from isceobj.Util import combinedlibmodule as CL
        orders, means, norms, coeffs = CL.importPoly2DFromC(pointer)
        self._azimuthOrder, self._rangeOrder = orders
        self._meanAzimuth, self._meanRange = means
        self._normAzimuth, self._normRange = norms
        self._coeffs = []

        for ii in range(self._azimuthOrder+1):
            ind = ii * (self._rangeOrder+1)
            self._coeffs.append(coeffs[ind:ind+self._rangeOrder+1])

        if clean:
            CL.freeCPoly2D(pointer)

        return

    def polyfit_numpy(self, x, y, z, w=None,maxOrder=True):
        '''
        Fit polynomials using numpy.
        '''

        if (len(x) != len(y)) or (len(x) != len(z)):
            raise ValueError('x, y and z should be of same length')

        if w:
            if len(z) != len(w):
                raise ValueError('w should be of same length as z')
            snr = w
        else:
            snr = np.ones(len(x))

        if (self._rangeOrder is None) or (self._azimuthOrder is None):
            raise ValueError('Order of 2D polynomial is undefined.')

        ymin = np.min(y)
        ynorm = np.max(y) - ymin
        if ynorm == 0:
            ynorm = 1.0

        y = (y-ymin)/ynorm

        xmin = np.min(x)
        xnorm = np.max(x) - xmin
        if xnorm == 0:
            xnorm = 1.0

        x = (x-xmin)/xnorm

        yOrder = self._azimuthOrder
        xOrder = self._rangeOrder

        if maxOrder: 
            bigOrder = max(yOrder, xOrder)

        arrList = []


        if maxOrder:
            for ii in range(min(yOrder,bigOrder)+1):
                yfact = np.power(y,ii)
                for kk in range(min(bigOrder-ii,xOrder)+1):
                    temp = np.power(x,kk)*yfact
                    arrList.append(temp.reshape((temp.size,1)))

        else:
            for ii in range(yOrder+1):
                yfact = np.power(y,ii)
                for kk in range(xOrder+1):
                    temp = np.power(x,kk)*yfact
                    arrList.append(temp.reshape((temp.size,1)))

        A = np.hstack(arrList)
        A = A / snr[:,None]
        b = z / snr

        val,res,rank,eigs = np.linalg.lstsq(A,b, rcond=1.0e-12)
#        print(res)
#        print('Chi: ', np.sqrt(res/(1.0*len(b))))

        self._meanRange = xmin
        self._meanAzimuth = ymin
        self._normRange = xnorm
        self._normAzimuth = ynorm


        for ii in range(yOrder+1):
            row = self._coeffs[ii]
            for jj in range(xOrder+1):
                row[jj] = 0.0

        if maxOrder:
            count = 0
            ii = 0

            for ii in range(min(yOrder,bigOrder)+1):
                row = self._coeffs[ii]
                for jj in range(min(bigOrder-ii,xOrder)+1):
                    row[jj] = val[count]
                    count += 1

        else:
            count = 0
            for ii in range(yOrder+1):
                row = self._coeffs[ii]
                for jj in range(xOrder+1):
                    row[jj] = val[count]
                    count += 1

        pass


def createPolynomial(order=None,
        norm=None, offset=None):
    '''
    Create a polynomial with given parameters.
    Order, Norm and Offset are iterables.
    '''

    poly = Polynomial(rangeOrder=order[0], azimuthOrder=order[1])

    if norm:
        poly.setNormRange(norm[0])
        poly.setNormAzimuth(norm[1])

    if offset:
        poly.setMeanRange(offset[0])
        poly.setMeanAzimuth(offset[1])

    return poly

def createRangePolynomial(order=None, offset=None, norm=None):
    '''
    Create a polynomial in range.
    '''
    poly = Polynomial(rangeOrder=order, azimuthOrder=0)

    if offset:
        poly.setMeanRange(offset)

    if norm:
        poly.setNormRange(norm)

    return poly

def createAzimuthPolynomial(order=None, offset=None, norm=None):
    '''
    Create a polynomial in azimuth.
    '''
    poly = Polynomial(rangeOrder=0, azimuthOrder=order)

    if offset:
        poly.setMeanAzimuth(offset)

    if norm:
        poly.setNormAzimuth(norm)

    return poly
