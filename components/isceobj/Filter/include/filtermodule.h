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




#ifndef filtermodule_h
#define filtermodule_h 1

#include <Python.h>
#include <complex>
#include "Image.hh"
#include "Filter.hh"
#include "header.h"

int meanFilterPhase(char *inFile, char *outFile, int imageWidth,
    int imageHeight,int filterWidth,int filterHeight);
int gaussianFilterPhase(char *inFile, char *outFile, int imageWidth,
    int imageHeight,int filterWidth,int filterHeight,double sigma);
int medianFilterPhase(char *inFile, char *outFile, int imageWidth,
    int imageHeight,int filterWidth,int filterHeight);

extern "C"
{
  PyObject *meanFilter_C(PyObject *self,PyObject *args);
  PyObject *gaussianFilter_C(PyObject *self,PyObject *args);
  PyObject *medianFilter_C(PyObject *self,PyObject *args);
}

static PyMethodDef filter_methods[] =
{
    {"meanFilter_Py",meanFilter_C,METH_VARARGS," "},
    {"gaussianFilter_Py",gaussianFilter_C,METH_VARARGS," "},
    {"medianFilter_Py",medianFilter_C,METH_VARARGS," "},
    {NULL,NULL,0,NULL}
};

#endif
