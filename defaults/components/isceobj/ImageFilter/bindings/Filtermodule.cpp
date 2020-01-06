//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Copyright: 2010 to the present, California Institute of Technology.
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
#include "FilterFactory.h"
#include "Filtermodule.h"
#include "DataAccessor.h"
#include <iostream>
#include <fstream>
#include <string>
#include <complex>
#include <stdint.h>
#include <cstdio>
using namespace std;

static char * const __doc__ = "module for Filter.cpp";

PyModuleDef moduledef = {
    // header
    PyModuleDef_HEAD_INIT,
    // name of the module
    "Filter",
    // module documentation string
    __doc__,
    // size of the per-interpreter state of the module;
    // -1 if this state is global
    -1,
    Filter_methods,
};

// initialization function for the module
// *must* be called PyInit_Filter
PyMODINIT_FUNC
PyInit_Filter()
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

PyObject * createFilter_C(PyObject* self, PyObject* args)
{
    string filter;
    char * filterCh;
    int selector;
    if(!PyArg_ParseTuple(args, "si",&filterCh,&selector))
    {
        return NULL;
    }
    filter = filterCh;
    FilterFactory * FF = new FilterFactory();
    uint64_t ptFilter = 0;

    ptFilter = (uint64_t ) FF->createFilter(filter,selector);
    delete FF;
    return Py_BuildValue("K",ptFilter);

}
PyObject * extract_C(PyObject* self, PyObject* args)
{
    uint64_t ptFilter = 0;
    if(!PyArg_ParseTuple(args, "K", &ptFilter))
    {
        return NULL;
    }
    ((Filter *) ptFilter)->extract();
    return Py_BuildValue("i", 0);
}
PyObject * finalize_C(PyObject* self, PyObject* args)
{
    uint64_t ptFilter = 0;
    if(!PyArg_ParseTuple(args, "K", &ptFilter))
    {
        return NULL;
    }
    ((Filter *) ptFilter)->finalize();
    delete (Filter *)ptFilter;
    return Py_BuildValue("i", 0);
}
PyObject * init_C(PyObject* self, PyObject* args)
{
    uint64_t ptFilter = 0;
    uint64_t ptAccessorIn = 0;
    uint64_t ptAccessorOut = 0;
    if(!PyArg_ParseTuple(args, "KKK", &ptFilter,&ptAccessorIn,&ptAccessorOut))
    {
        return NULL;
    }
    ((Filter *) ptFilter)->init((DataAccessor *)ptAccessorIn,
        (DataAccessor *) ptAccessorOut);
    return Py_BuildValue("i", 0);
}
PyObject * selectBand_C(PyObject* self, PyObject* args)
{
    uint64_t ptFilter = 0;
    int band = 0;
    if(!PyArg_ParseTuple(args, "Ki", &ptFilter,&band))
    {
        return NULL;
    }
    ((Filter *) ptFilter)->selectBand(band);
    return Py_BuildValue("i", 0);
}
PyObject * setStartLine_C(PyObject* self, PyObject* args)
{
    uint64_t ptFilter = 0;
    int line = 0;
    if(!PyArg_ParseTuple(args, "Ki", &ptFilter,&line))
    {
        return NULL;
    }
    ((Filter *) ptFilter)->setStartLine(line);
    return Py_BuildValue("i", 0);
}
PyObject * setEndLine_C(PyObject* self, PyObject* args)
{
    uint64_t ptFilter = 0;
    int line = 0;
    if(!PyArg_ParseTuple(args, "Ki", &ptFilter,&line))
    {
        return NULL;
    }
    ((Filter *) ptFilter)->setEndLine(line);
    return Py_BuildValue("i", 0);
}
