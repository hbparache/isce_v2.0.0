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





class Polynomial(object):
    '''
    Class to store 1D polynomials in ISCE.
    Implented as a list of coefficients:

    [    1,     x^1,     x^2, ...., x^n]

    The size of the 1D list will correspond to 
    [order+1].
    '''

    def __init__(self, order=None):
        '''
        Constructor for the polynomial object.
        '''
        self._coeffs = []
        if order:
            for k in range(order+1):
                self._coeffs.append(0.)

            self._order = int(order)
        else:
            self._order = None
        self._norm = 1.0
        self._mean = 0.0
        
        return

    def setCoeffs(self, parms):
        '''
        Set the coefficients using another nested list.
        '''
        for ii,row in enumerate(parms):
            self._coeffs[ii] = float(row)

        return

    def getCoeffs(self):
        return self._coeffs

    def setNorm(self, parm):
        self._norm = float(parm)

    def getNorm(self):
        return self._norm

    def __call__(self, rng):
        '''
        Evaluate the polynomial.
        This is much slower than the C implementation - only for sparse usage.
        '''
        x = (rng - self._mean)/self._norm
        res = 0.
        for ii,row in enumerate(self._coeffs):
            res += row * (x**ii)

        return res

    def exportToC(self):
        '''
        Use the extension module and return a pointer in C.
        '''
        from isceobj.Util import combinedlibmodule as CL

        g = CL.exportPoly1DToC(self._order, self._mean, self._norm, self._coeffs)
        print(g)

        return g

    def importFromC(self, pointer, clean=True):
        ''' 
        Uses information from the  extension module structure to create Python object.
        '''
        from isceobj.Util import combinedlibmodule as CL

        order,mean,norm,coeffs = CL.importPoly1DFromC(pointer)
        self._order = order
        self._mean = mean
        self._norm = norm
        self._coeffs = coeffs.copy()

        if clean:
            CL.freeCPoly1D(pointer)
        pass
        
def createPolynomial(order=None,
        norm=None, offset=None):
    '''
    Create a polynomial with given parameters.
    Order, Norm and Offset are iterables.
    '''
    
    poly = Polynomial(order=order)

    if norm:
        poly.setNorm(norm)

    if offset:
        poly.setMean(offset)
        
    return poly

