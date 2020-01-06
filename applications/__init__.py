## The appications:
__all__ = ['CalculatePegPoint',
           'calculateBaseline',
           'createGeneric',
           'dpmApp',
           'extractHDROrbit',
           'focus',
           'formSLC',
           'insarApp',
           'isce.log',
           'make_input',
           'make_raw',
           'mdx',
           'readdb',
           'viewMetadata',
           'xmlGenerator']
def createInsar():
    from .insarApp import Insar
    return Insar()

def getFactoriesInfo():
     return  {'Insar':
                     {
                     'factory':'createInsar'                     
                     }
              }
