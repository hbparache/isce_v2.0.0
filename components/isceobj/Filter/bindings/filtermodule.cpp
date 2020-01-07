//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Copyright: 2012 to the present, California Institute of Technology.
// ALL RIGHTS RESERVED. United States Government Sponsorship acknowledged.
// Any commercial use must be negotiated with the Office of Technology Transfer
// at the California Institute of Technology.
// 
// This software may be subject to U.S. export control laws. By accepting this
// software, the user agrees to comply with all applicable U.S. export laws and
// regulations. User has the responsibility to obtain export licenses,  or other
// export authority as may be required before exporting such information to
// foreign countries or providing access to foreign persons.
// 
// Installation and use of this software is restricted by a license agreement
// between the licensee and the California Institute of Technology. It is the
// User's responsibility to abide by the terms of the license agreement.
//
// Author: Giangi Sacco
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




#include <Python.h>
#include "filtermodule.h"

// A C++ extension is required for this code since
// ctypes does not currently allow interfacing with C++ code
// (name-mangling and all).

static const char * __doc__ = "module for filter.F";

PyModuleDef moduledef = {
    // header
    PyModuleDef_HEAD_INIT,
    // name of the module
    "filter",
    // module documentation string
    __doc__,
    // size of the per-interpreter state of the module;
    // -1 if this state is global
    -1,
    filter_methods,
};

// initialization function for the module
// *must* be called PyInit_filter
PyMODINIT_FUNC
PyInit_filter()
{
    // create the module using moduledef struct defined above
    PyObject * module = PyModule_Create(&moduledef);
    // check whether module creation succeeded and raise an exception if not
    if (!module) {
        return module;
    }
    // otherwise, we have an initialized module
    // and return the newly created module
    return module;
}

PyObject *meanFilter_C(PyObject *self, PyObject *args)
{
  char *inFile,*outFile;
  int status,filterWidth,filterHeight,imageWidth,imageHeight;

  if(!PyArg_ParseTuple(args, "ssiiii", &inFile, &outFile, &imageWidth,
        &imageHeight,&filterWidth,&filterHeight))
    {
      return NULL;
    }

  status = meanFilterPhase(inFile, outFile, imageWidth, imageHeight,
               filterWidth,filterHeight);

  return Py_BuildValue("i",0);
}

PyObject *gaussianFilter_C(PyObject *self, PyObject *args)
{
  char *inFile,*outFile;
  int status,filterWidth,filterHeight,imageWidth,imageHeight;
  double sigma;

  if(!PyArg_ParseTuple(args, "ssiiiid", &inFile, &outFile, &imageWidth,
        &imageHeight,&filterWidth,&filterHeight,&sigma))
  {
      return NULL;
  }

  status = gaussianFilterPhase(inFile, outFile, imageWidth, imageHeight,
               filterWidth,filterHeight,sigma);

  return Py_BuildValue("i",0);
}

PyObject *medianFilter_C(PyObject *self, PyObject *args)
{
  char *inFile,*outFile;
  int status,filterWidth,filterHeight,imageWidth,imageHeight;

  if(!PyArg_ParseTuple(args, "ssiiii", &inFile, &outFile, &imageWidth,
       &imageHeight,&filterWidth,&filterHeight))
  {
      return NULL;
  }

  status = medianFilterPhase(inFile, outFile, imageWidth, imageHeight,
               filterWidth, filterHeight);

  return Py_BuildValue("i",0);
}
