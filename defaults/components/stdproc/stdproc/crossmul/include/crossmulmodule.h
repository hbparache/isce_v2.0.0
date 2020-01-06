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




#ifndef crossmulmodule_h
#define crossmulmodule_h

#include <Python.h>
#include <stdint.h>
#include "crossmul.h"

extern "C"
{
    PyObject * createCrossMul_C(PyObject *, PyObject *);
    PyObject * setWidth_C(PyObject *, PyObject *);
    PyObject * setLength_C(PyObject *, PyObject *);
    PyObject * setLooksAcross_C(PyObject *, PyObject *);
    PyObject * setLooksDown_C(PyObject *, PyObject *);
    PyObject * setScale_C(PyObject *, PyObject *);
    PyObject * setBlocksize_C(PyObject *, PyObject *);
    void crossmul_f(crossmulState*, uint64_t*, uint64_t*, uint64_t*,
        uint64_t*);
    PyObject * crossmul_C(PyObject*, PyObject*);
    PyObject * destroyCrossMul_C(PyObject *, PyObject *);

}

static PyMethodDef crossmul_methods[] =
{
     {"createCrossMul_Py", createCrossMul_C, METH_VARARGS, " "},
     {"destroyCrossMul_Py", destroyCrossMul_C, METH_VARARGS, " "},
     {"setWidth_Py", setWidth_C, METH_VARARGS, " "},
     {"setLength_Py", setLength_C, METH_VARARGS, " "},
     {"setLooksAcross_Py", setLooksAcross_C, METH_VARARGS, " "},
     {"setLooksDown_Py", setLooksDown_C, METH_VARARGS, " "},
     {"setScale_Py", setScale_C, METH_VARARGS, " "},
     {"setBlocksize_Py", setBlocksize_C, METH_VARARGS, " "},
     {"crossmul_Py", crossmul_C, METH_VARARGS, " "},
     {NULL, NULL, 0, NULL}
};
#endif

// end of file
