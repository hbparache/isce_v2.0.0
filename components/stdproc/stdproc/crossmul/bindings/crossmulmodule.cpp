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
#include "crossmul.h"
#include "crossmulmodule.h"
#include <stdint.h>
using namespace std;

static char * const __doc__ = "Python extension for crossmul.F";

PyModuleDef moduledef = {
    //header
    PyModuleDef_HEAD_INIT,
    //name of the module
    "crossmul",
    //module documentation string
    __doc__,
    //size of the per-interpreter state of the module
    //-1 if this state is global
    -1,
    crossmul_methods,
};

//initialization function for the module
//// *must* be called PyInit_crossmul
PyMODINIT_FUNC
PyInit_crossmul()
{
    //create the module using moduledef struct defined above
    PyObject * module = PyModule_Create(&moduledef);
    //check whether module create succeeded and raise exception if not
    if(!module)
    {
        return module;
    }
    //otherwise we have an initialized module
    //and return the newly created module
    return module;
}

PyObject * createCrossMul_C(PyObject* self, PyObject* args)
{
    crossmulState* newObj = new crossmulState;
    return Py_BuildValue("K", (uint64_t) newObj);
}

PyObject * destroyCrossMul_C(PyObject* self, PyObject* args)
{
    uint64_t ptr;
    if(!PyArg_ParseTuple(args,"K",&ptr))
    {
        return NULL;
    }
    if ((crossmulState*)(ptr) != NULL)
    {
        delete ((crossmulState*)(ptr));
    }
}

PyObject * setWidth_C(PyObject* self, PyObject* args)
{
    int var;
    uint64_t ptr;
    if(!PyArg_ParseTuple(args, "Ki", &ptr, &var))
    {
        return NULL;
    }
    ((crossmulState*)(ptr))->na = var;
    return Py_BuildValue("i", 0);
}

PyObject * setLength_C(PyObject* self, PyObject* args)
{
    int var;
    uint64_t ptr;
    if(!PyArg_ParseTuple(args, "Ki", &ptr, &var))
    {
        return NULL;
    }
    ((crossmulState*)(ptr))->nd = var;
    return Py_BuildValue("i", 0);
}

PyObject * setLooksAcross_C(PyObject* self, PyObject* args)
{
    int var;
    uint64_t ptr;
    if(!PyArg_ParseTuple(args, "Ki", &ptr, &var))
    {
        return NULL;
    }
    ((crossmulState*)(ptr))->looksac = var;
    return Py_BuildValue("i", 0);
}

PyObject * setLooksDown_C(PyObject* self, PyObject* args)
{
    int var;
    uint64_t ptr;
    if(!PyArg_ParseTuple(args, "Ki", &ptr, &var))
    {
        return NULL;
    }
    ((crossmulState*)(ptr))->looksdn = var;
    return Py_BuildValue("i", 0);
}


PyObject * setScale_C(PyObject* self, PyObject* args)
{
    double var;
    uint64_t ptr;
    if(!PyArg_ParseTuple(args, "Kd", &ptr, &var))
    {
        return NULL;
    }
    ((crossmulState*)(ptr))->scale = var;
    return Py_BuildValue("i", 0);
}

PyObject * setBlocksize_C(PyObject* self, PyObject* args)
{
    int var;
    uint64_t ptr;
    if(!PyArg_ParseTuple(args, "Ki", &ptr, &var))
    {
        return NULL;
    }
    ((crossmulState*)(ptr))->blocksize =  var;
    return Py_BuildValue("i", 0);
}


PyObject * crossmul_C(PyObject *self, PyObject *args)
{
    uint64_t state;
    uint64_t slc1, slc2, ifg, amp;
    if (!PyArg_ParseTuple(args,"KKKKK", &state, &slc1, &slc2, &ifg, &amp))
    {
        return NULL;
    }
    crossmul_f((crossmulState*)(state), &slc1, &slc2, &ifg, &amp);
    return Py_BuildValue("i", 0);
}
