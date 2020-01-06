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
# Author: Eric Gurrola
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




from contextlib import contextmanager



__all__ = ("createCoordinate", 
           "createImage", 
           "createRawImage", 
           "createStreamImage", 
           "createSlcImage", 
           "createRgImage", 
           "createIntImage", 
           "createAmpImage", 
           "createOffsetImage", 
           "createDemImage",
           "contextIntImage",
           "contextOffsetImage",
           "contextRawImage",
           "contextStreamImage",
           "contextSlcImage",
           "contextRgImage",
           "contextAmpImage",
           "contextOffsetImage",
           "contextUnwImage",
           "contextAnyImage")



## Decorator to make image factroies into contextmanagers
def image_context(factory):
    @contextmanager
    def context_factory(filename=None, width=None, accessMode=None, create=True):
        """ %s image factory. Keywords arguments:

        kwarg            action
        -----------------------------------
        filename         setFilename
        width            setWidth
        accessMode       setFilename
        [create=True]    --call Image.createImage() -if all key
                           words are set
        """
        ## ONE: Build the context up:
        result = factory()
        if filename is not None:
            result.setFilename(filename)
        if width is not None:
            result.setWidth(width)
        if accessMode is not None:
            result.setAccessMode(accessMode)
        if width and filename and accessMode and create:
            result.createImage()

        yield result
        ## TWO: Tear it back down.
        result.finalizeImage()
        pass
    ## prepare context manager's docstring
    context_factory.__doc__ =  context_factory.__doc__  % (factory.__name__)
    return context_factory


def createCoordinate():
    from .Image import ImageCoordinate
    return ImageCoordinate()
def createImage(name=''):
    from .Image import Image
    return Image(name)

def createRawImage():
    from .RawImage import RawImage
    return RawImage()

def createStreamImage():
    from .StreamImage import StreamImage
    return StreamImage()

def createSlcImage():
    from .SlcImage import SlcImage
    return SlcImage()

def createRgImage():
    from .RgImage import RgImage
    return RgImage()

def createIntImage():
    from .IntImage import IntImage
    return IntImage()

def createAmpImage():
    from .AmpImage import AmpImage
    return AmpImage()
def createOffsetImage():
    from .OffsetImage import OffsetImage
    return OffsetImage()
def createDemImage(name=''):
    from .DemImage import DemImage
    return DemImage(name)
def createUnwImage():
    from .UnwImage import UnwImage
    return UnwImage()

## This is the IntImage factory's contect manager
contextIntImage = image_context(createIntImage)
contextRawImage = image_context(createRawImage)
contextStreamImage = image_context(createStreamImage)
contextSlcImage = image_context(createSlcImage)
contextRgImage = image_context(createRgImage)
contextAmpImage = image_context(createAmpImage)
contextOffsetImage = image_context(createOffsetImage)
contextDemImage = image_context(createDemImage)
contextUnwImage = image_context(createUnwImage)

## This manger takes a cls or instance, calls it factory in a context manager
@contextmanager
def contextAnyImage(cls,
               filename=None, width=None, accessMode=None, create=True):
    """imageFactory(cls,
                    filename=None, width=None, accessMode=None, create=True):

       cls:     as class OR instance of an Image subclass.

       returns a context manager that creates the class in a context.
       Keyword arguments are passed to the context manager, and are 
       use to build the class up.
       """
    if not isinstance(cls, type):
        cls = cls.__class__
        
    cls_name = cls.__name__

    hash_table = {
 'RawImage' : createRawImage,
 'StreamImage' : createStreamImage,
 'SlcImage' : createSlcImage,
 'RgImage' : createRgImage,
 'IntImage' : createIntImage,
 'AmpImage' : createAmpImage,
 'OffsetImage' : createOffsetImage,
 'DemImage' : createDemImage,
 'UnwImage' : createUnwImage
 }
    try:
        factory =  hash_table[cls_name]
    except KeyError:
        raise TypeError('Cannot find factory for: %s' % cls_name)

    ## ONE: Build the context up:
    result = factory()
    if filename is not None:
        result.setFilename(filename)
    if width is not None:
        result.setWidth(width)
    if accessMode is not None:
        result.setAccessMode(accessMode)
    if width and filename and accessMode and create:
        result.createImage()

    yield result
    try:
        result.finalizeImage()
    except TypeError:
        print("Image was not initialized, so finalizeImage failed")
    pass
