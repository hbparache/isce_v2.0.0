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
# Author: Eric Belz
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




"""eRdf Experimental RDF stuff- no warranty"""
## \namespace rdf.eRDF __e__ xperimental RDF objects



## A generic base class for RDF wrapped data structures -clients should
## use this when they have an object with RDF dependency injection and then
## further behavior as defined by the sub-classes methods.
class RDFWrapper(object):
    """RDFWrapper(rdf instance):

    is a base class for classes that wrap rdf instances.
    """
    
    ## Initialized with an RDF instance
    ## \param rdf_ a bonafide rdf.data.files.RDF object
    def __init__(self, rdf_):
        ## The wrapped rdf 
        self._rdf = rdf_
        return None
    
    ## self.rdf == self.rdf() == self._rdf
    @property
    def rdf(self):
        return self._rdf

    ## Access rdf dictionary
    def __getitem__(self, key):
        return self._rdf.__getitem__(self, key)
    
    ## Access rdf dictionary
    def __setitem__(self, key, field):
        return self._rdf.__setitem__(self, key, field)
    
    ## Access rdf dictionary
    def __delitem__(self, key):
        return self._rdf.__delitem__(self, key)
    
    ## Access rdf dictionary
    def __len__(self, key):
        return len(self._rdf)
    
    
    
## Experimental function to factor keys and rdf.
def factor(rdf_):
    _k = rdf_.keys()
    _k.sort()
    k = _k[:]
    longest = max(map(len, k))
    import numpy as np
    m = np.zeros( (len(k), 27 ), dtype=int )
    for jdx, key in enumerate(k):
        for idx, cc in enumerate(key):
            m[jdx, idx] = ord(cc)
    base = [2**__ for __ in map(long, range(len(m[0])))]
    

