//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Copyright: 2011 to the present, California Institute of Technology.
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




#ifndef dismphfilemodule_h
#define dismphfilemodule_h

#include <Python.h>
#include <stdint.h>
#include "dismphfilemoduleFortTrans.h"

extern "C"
{
    void dismphfile_f(uint64_t *, uint64_t *);
    PyObject * dismphfile_C(PyObject *, PyObject *);
    void setLength_f(int *);
    PyObject * setLength_C(PyObject *, PyObject *);
    void setFirstLine_f(int *);
    PyObject * setFirstLine_C(PyObject *, PyObject *);
    void setNumberLines_f(int *);
    PyObject * setNumberLines_C(PyObject *, PyObject *);
    void setFlipFlag_f(int *);
    PyObject * setFlipFlag_C(PyObject *, PyObject *);
    void setScale_f(float *);
    PyObject * setScale_C(PyObject *, PyObject *);
    void setExponent_f(float *);
    PyObject * setExponent_C(PyObject *, PyObject *);

}

static PyMethodDef dismphfile_methods[] =
{
    {"dismphfile_Py", dismphfile_C, METH_VARARGS, " "},
    {"setLength_Py", setLength_C, METH_VARARGS, " "},
    {"setFirstLine_Py", setFirstLine_C, METH_VARARGS, " "},
    {"setNumberLines_Py", setNumberLines_C, METH_VARARGS, " "},
    {"setFlipFlag_Py", setFlipFlag_C, METH_VARARGS, " "},
    {"setScale_Py", setScale_C, METH_VARARGS, " "},
    {"setExponent_Py", setExponent_C, METH_VARARGS, " "},
    {NULL, NULL, 0, NULL}
};
#endif dismphfilemodule_h
