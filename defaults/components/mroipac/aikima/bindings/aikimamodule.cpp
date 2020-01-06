//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Copyright: 2013 to the present, California Institute of Technology.
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
// Author: Piyush Agram
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#include <Python.h>
#include "aikimamodule.h"
#include <sstream>
#include <iostream>
#include <fstream>
using namespace std;

static char * const __doc__ = "Python extension for aikima";

PyModuleDef moduledef = {
    // header
    PyModuleDef_HEAD_INIT,
    // name of the module
    "aikima",
    // module documentation string
    __doc__,
    // size of the per-interpreter state of the module;
    // -1 if this state is global
    -1,
    aikima_methods,
};

// initialization function for the module
PyMODINIT_FUNC
PyInit_aikima()
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


//Create the python wrapper function that interfaces to the c/fortran function
PyObject * aikima_C(PyObject *self, PyObject *args)
{
    //temporary variables to handle the arguments passed from python
    uint64_t imgin;
    uint64_t imgout;
    int inband, outband;
    if(!PyArg_ParseTuple(args, "KKii", &imgin, &imgout, &inband, &outband))
    {
        return NULL;
    }
    
    //make the actual call
    aikima_f(&imgin, &imgout, &inband, &outband);

   //return success
   return Py_BuildValue("i", 0);
}


PyObject* setWidth_C(PyObject* self, PyObject* args)
{
    int width;
    if(!PyArg_ParseTuple(args,"i", &width))
    {
        return NULL;
    }

    setWidth_f(&width);
    return Py_BuildValue("i",0);
}

PyObject* setLength_C(PyObject* self, PyObject* args)
{
    int width;
    if(!PyArg_ParseTuple(args,"i",&width))
    {
        return NULL;
    }

    setLength_f(&width);
    return Py_BuildValue("i",0);
}

PyObject* setBlockSize_C(PyObject* self, PyObject* args)
{
    int width;
    if(!PyArg_ParseTuple(args,"i",&width))
    {
        return NULL;
    }

    setBlockSize_f(&width);
    return Py_BuildValue("i",0);
}

PyObject* setPadSize_C(PyObject* self, PyObject* args)
{
    int width;
    if(!PyArg_ParseTuple(args,"i",&width))
    {
        return NULL;
    }

    setPadSize_f(&width);
    return Py_BuildValue("i",0);
}

PyObject* setFirstPixelAcross_C(PyObject* self, PyObject* args)
{
    int width;
    if(!PyArg_ParseTuple(args,"i",&width))
    {
        return NULL;
    }

    width = width+1;
    setFirstPixelAcross_f(&width);
    return Py_BuildValue("i",0);
}

PyObject* setLastPixelAcross_C(PyObject* self, PyObject* args)
{
    int width;
    if(!PyArg_ParseTuple(args,"i",&width))
    {
        return NULL;
    }

    setLastPixelAcross_f(&width);
    return Py_BuildValue("i",0);
}


PyObject* setFirstLineDown_C(PyObject* self, PyObject* args)
{
    int width;
    if(!PyArg_ParseTuple(args,"i",&width))
    {
        return NULL;
    }
    width = width+1;
    setFirstLineDown_f(&width);
    return Py_BuildValue("i",0);
}

PyObject* setLastLineDown_C(PyObject* self, PyObject* args)
{
    int width;
    if(!PyArg_ParseTuple(args,"i",&width))
    {
        return NULL;
    }

    setLastLineDown_f(&width);
    return Py_BuildValue("i",0);
}

PyObject* setNumberPtsPartial_C(PyObject* self, PyObject* args)
{
    int width;
    if(!PyArg_ParseTuple(args,"i",&width))
    {
        return NULL;
    }

    setNumberPtsPartial_f(&width);
    return Py_BuildValue("i",0);
}

PyObject* setPrintFlag_C(PyObject* self, PyObject* args)
{
    int width;
    if(!PyArg_ParseTuple(args,"i",&width))
    {
        return NULL;
    }

    setPrintFlag_f(&width);
    return Py_BuildValue("i",0);
}

PyObject* setThreshold_C(PyObject* self, PyObject* args)
{
    float width;
    if(!PyArg_ParseTuple(args,"f",&width))
    {
        return NULL;
    }

    setThreshold_f(&width);
    return Py_BuildValue("i",0);
}

