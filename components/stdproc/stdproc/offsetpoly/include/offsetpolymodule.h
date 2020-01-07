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




#ifndef offsetpolymodule_h
#define offsetpolymodule_h

#include <Python.h>
#include <stdint.h>
#include "offsetpolymoduleFortTrans.h"

extern "C"
{
    void offsetpoly_f();
    PyObject * offsetpoly_C(PyObject *, PyObject *);

    void allocateFieldArrays_f(int *);
    PyObject *allocateFieldArrays_C(PyObject *, PyObject *);

    void deallocateFieldArrays_f();
    PyObject *deallocateFieldArrays_C(PyObject *, PyObject *);

    void allocatePolyArray_f(int *);
    PyObject *allocatePolyArray_C(PyObject *, PyObject *);

    void deallocatePolyArray_f();
    PyObject *deallocatePolyArray_C(PyObject *, PyObject *);

    PyObject * setLocationAcross_C(PyObject *, PyObject *);
    void setLocationAcross_f(double *, int *);

    void setOffset_f(double *, int *);
    PyObject * setOffset_C(PyObject *, PyObject*);


    void setLocationDown_f(double *, int *);
    PyObject * setLocationDown_C(PyObject *, PyObject *);


    void setSNR_f(double *, int *);
    PyObject * setSNR_C(PyObject *, PyObject *);

    PyObject* getOffsetPoly_C(PyObject*, PyObject *);
    void getOffsetPoly_f(double *, int *);
}

static PyMethodDef offsetpoly_methods[] =
{
    {"offsetpoly_Py", offsetpoly_C, METH_VARARGS, " "},
    {"setLocationAcross_Py", setLocationAcross_C, METH_VARARGS, " "},
    {"setOffset_Py", setOffset_C, METH_VARARGS, " "},
    {"setLocationDown_Py", setLocationDown_C, METH_VARARGS, " "},
    {"setSNR_Py", setSNR_C, METH_VARARGS, " "},
    {"allocateFieldArrays_Py", allocateFieldArrays_C, METH_VARARGS, " "},
    {"deallocateFieldArrays_Py", deallocateFieldArrays_C, METH_VARARGS, " "},
    {"allocatePolyArray_Py", allocatePolyArray_C, METH_VARARGS, " "},
    {"deallocatePolyArray_Py", deallocatePolyArray_C, METH_VARARGS, " "},
    {"getOffsetPoly_Py", getOffsetPoly_C, METH_VARARGS, " "},
    {NULL, NULL, 0, NULL}
};
#endif
// end of file
