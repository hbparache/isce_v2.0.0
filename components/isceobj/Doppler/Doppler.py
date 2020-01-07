#!/usr/bin/env python3 

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




class Doppler(object):

    def __init__(self, prf=0):
        """A class to hold Doppler polynomial coefficients.

        @note The polynomial is expected to be referenced to range bin.

        @param prf The pulse repetition frequency [Hz]
        @param ambigutiy The integer ambiguity of the Doppler centroid
        @param fractionalCentroid The fractional part of the Doppler centroid
        [Hz/PRF]
        @param linearTerm The linear term in the Doppler vs. range polynomical
        [Hz/PRF]
        @param quadraticTerm The quadratic term in the Doppler vs. range
        polynomical [Hz/PRF]
        @param cubicTerm The cubic term in the Doppler vs. range polynomical
        [Hz/PRF]
        """
        self.prf = prf
        self.ambiguity = 0
        self.fractionalCentroid = 0.0
        self.linearTerm = 0.0
        self.quadraticTerm = 0.0
        self.cubicTerm = 0.0
        self.numCoefs = 4
        return

    def getDopplerCoefficients(self,inHz=False):
        """Get the Doppler polynomial coefficients as a function of range,
        optionally scaled by the PRF.

        @param inHz (\a boolean) True if the returned coefficients should
        have units of Hz, False if the "units" should be Hz/PRF
        @return the Doppler polynomial coefficients as a function of range.
        """
        coef = [self.ambiguity+self.fractionalCentroid,
                self.linearTerm,
                self.quadraticTerm,
                self.cubicTerm]
        if inHz:
            coef = [x*self.prf for x in coef]

        return coef

    def setDopplerCoefficients(self, coef, ambiguity=0, inHz=False):
        """Set the Doppler polynomial coefficients as a function of range.

        @param coef a list containing the cubic polynomial Doppler
        coefficients as a function of range
        @param ambiguity (\a int) the absolute Doppler ambiguity
        @param inHz (\a boolean) True if the Doppler coefficients have units
        of Hz, False if the "units" are Hz/PRF
        """
        if inHz and (self.prf != 0.0):
            coef = [x/self.prf for x in coef]

        self.fractionalCentroid = coef[0] - self.ambiguity
        self.linearTerm = coef[1]
        self.quadraticTerm = coef[2]
        self.cubicTerm = coef[3]

    def average(self, *others):
        """Average my Doppler with other Doppler objects"""
        from operator import truediv
        n = 1 + len(others)
        prfSum = self.prf
        coefSum = self.getDopplerCoefficients(inHz=True)
        for e in others:
            prfSum += e.prf
            otherCoef = e.getDopplerCoefficients(inHz=True)
            for i in range(self.numCoefs): coefSum[i] += otherCoef[i]

        prf = truediv(prfSum, n)
        coef = [truediv(coefSum[i], n) for i in range(self.numCoefs)]
        averageDoppler = self.__class__(prf=prf)
        averageDoppler.setDopplerCoefficients(coef, inHz=True)

        return averageDoppler

    def evaluate(self, rangeBin=0, inHz=False):
        """Calculate the Doppler in a particular range bin by evaluating the
        Doppler polynomial."""
        dop = (
            (self.ambiguity + self.fractionalCentroid) +
            self.linearTerm*rangeBin + 
            self.quadraticTerm*rangeBin**2 + self.cubicTerm*rangeBin**3
            )

        if inHz:
            dop = dop*self.prf

        return dop

    ## An obvious overload?
    def __call__(self, rangeBin=0, inHz=False):
        return self.evaluate(rangeBin=rangeBin, inHz=inHz)

    ## Convert to a standard numpy.poly1d object
    def poly1d(self, inHz=False):
        from numpy import poly1d, array
        if inHz:
            factor = 1./self.prf
            variable = 'Hz'
        else:
            factor = 1.
            variable = 'PRF'
            
        return poly1d(array([
                    self.cubicTerm,
                    self.quadraticTerm,
                    self.linearTerm,
                    (self.ambiguity + self.fractionalCentroid)
                    ]) * factor, variable=variable)

    def __str__(self):
        retstr = "PRF: %s\n"
        retlst = (self.prf,)
        retstr += "Ambiguity: %s\n"
        retlst += (self.ambiguity,)
        retstr += "Centroid: %s\n"
        retlst += (self.fractionalCentroid,)
        retstr += "Linear Term: %s\n"
        retlst += (self.linearTerm,)
        retstr += "Quadratic Term: %s\n"
        retlst += (self.quadraticTerm,)
        retstr += "Cubic Term: %s\n"
        retlst += (self.cubicTerm,)
        return retstr % retlst
