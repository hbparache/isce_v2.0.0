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





#ifndef calc_dopmodule_h
#define calc_dopmodule_h

#include <Python.h>
#include <stdint.h>
#include "calc_dopmoduleFortTrans.h"

extern "C"
{
    void calc_dop_f(uint64_t *);
    PyObject * calc_dop_C(PyObject *, PyObject *);
    void setHeader_f(int *);
    PyObject * setHeader_C(PyObject *, PyObject *);
    void setWidth_f(int *);
    PyObject * setWidth_C(PyObject *, PyObject *);
    void setLastLine_f(int *);
    PyObject * setLastLine_C(PyObject *, PyObject *);
    void setFirstLine_f(int *);
    PyObject * setFirstLine_C(PyObject *, PyObject *);
    void setIoffset_f(double *);
    PyObject * setIoffset_C(PyObject *, PyObject *);
    void setQoffset_f(double *);
    PyObject * setQoffset_C(PyObject *, PyObject *);
    void getRngDoppler_f(double *, int *);
    void allocate_rngDoppler_f(int *);
    void deallocate_rngDoppler_f();
    PyObject * allocate_rngDoppler_C(PyObject *, PyObject *);
    PyObject * deallocate_rngDoppler_C(PyObject *, PyObject *);
    PyObject * getRngDoppler_C(PyObject *, PyObject *);
    void getDoppler_f(double *);
    PyObject * getDoppler_C(PyObject *, PyObject *);
}

static PyMethodDef calc_dop_methods[] =
{
    {"calc_dop_Py", calc_dop_C, METH_VARARGS, " "},
    {"setHeader_Py", setHeader_C, METH_VARARGS, " "},
    {"setWidth_Py", setWidth_C, METH_VARARGS, " "},
    {"setLastLine_Py", setLastLine_C, METH_VARARGS, " "},
    {"setFirstLine_Py", setFirstLine_C, METH_VARARGS, " "},
    {"setIoffset_Py", setIoffset_C, METH_VARARGS, " "},
    {"setQoffset_Py", setQoffset_C, METH_VARARGS, " "},
    {"allocate_rngDoppler_Py", allocate_rngDoppler_C, METH_VARARGS, " "},
    {"deallocate_rngDoppler_Py", deallocate_rngDoppler_C, METH_VARARGS, " "},
    {"getRngDoppler_Py", getRngDoppler_C, METH_VARARGS, " "},
    {"getDoppler_Py", getDoppler_C, METH_VARARGS, " "},
    {NULL, NULL, 0, NULL}
};
#endif calc_dopmodule_h
