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
# Author: Eric Belz
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



"""A very simple 1st order differentiator"""
## \namespace ::geo::dxdt  A simple differentiator

## numerical derivative algorithm \n
## see http://docs.scipy.org/doc/scipy/reference/misc.html for other
## functions (maybe better).
def deriv(x,y=None):
    """(dy/dx) = deriv(x [,y=None])"""
    import numpy
    
    if y is None: return deriv(numpy.arange(len(x), dtype=float), x)
    
    n = len(x)
    if n < 3:
        print('Parameters must have at least 3 points')
        raise ValueError
    
    if n != len(y):
        print('x and y must have same length')
        raise ValueError
    
    Sleft = Shifter(1)
    Sright = ~Sleft
    
    x12 = x - Sleft(x)   #x1 - x2
    x01 = Sright(x) - x    #x0 - x1
    x02 = Sright(x) - Sleft(x) #x0 - x2
    
    
    d = (Sright(y) * (x12 / (x01*x02)) +  y * (1./x12 - 1./x01) - Sleft(y) * (x01 / (x02 * x12)))
    
    
    d[0] = y[0] * (x01[1]+x02[1])/(x01[1]*x02[1]) - y[1] * x02[1]/(x01[1]*x12[1]) + y[2] * x01[1]/(x02[1]*x12[1])
    n2 = n-2
    d[n-1] = -y[n-3] * x12[n2]/(x01[n2]*x02[n2]) + y[n-2] * x02[n2]/(x01[n2]*x12[n2]) -y[n-1] * (x02[n2]+x12[n2]) / (x02[n2]*x12[n2])
    
    return d


## integer index shift of an array \f$ x'_i = x_{(i+n)\, \bmod\, {\rm len}\, x} \f$, with wrapping
def ishift(x, m=0):
    """shift index, e.g.:
    In [4]: dsp.ishift([0,1,2,3,4,5], 2)
    Out[4]: [2, 3, 4, 5, 0, 1] """
    import numpy
    L = len(x)
    y = numpy.zeros_like(x)
    n = m%L
    y[:L-n] = x[n:]
    y[L-n:] = x[:n]
    return y


## \f$ [S_n(x)]_i \rightarrow x_{i+n} \f$ \n Shifter wraps ishift() ir fshift() with fixed n as a circular buffer  (http://en.wikipedia.org/wiki/Circular_buffer ) \n For fixed length, the frequency domain phase ramp is precomputed, so it will be faster for repeated use.
class Shifter(object):

    ## number of indices to shift:
    def __init__(self, n, length = None):
        ## \f$n\f$ is the number of indices to shift
        self.n = n
        self.length = length
        if isinstance(n, (int, long)):
            F = lambda x: ishift(x, self.n)
        else:
            if length is None:
                F = lambda x: fshift(x, self.n)
            else:
                f_shifter = fshifter(self.length, self.n)
                F = lambda x: fftpack.ifft(fftpack.fft(x)*f_shifter)
            pass
        
        self.F = F

        return None
    
    ## int(self) = self.n
    def __int__(self):
        return self.n

    ## float(self) = self.n
    def __float__(self):
        return self.n

    ## len(self) = self.length, which is optional\n If self.length is not None, then the shifter is created at __init__(), not __call__().
    def __len__(self):
        return self.length if self.length else 0

    ## inverse shift
    def __invert__(self):
        return self.__class__(-self.n)

    ## self(n)(x) = ::ishift(x, self.n)
    def __call__(self, x):
        return self.F(x)
    
    pass

