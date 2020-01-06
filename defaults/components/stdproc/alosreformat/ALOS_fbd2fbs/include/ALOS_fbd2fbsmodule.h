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




#ifndef ALOS_fbd2fbsmodule_h
#define ALOS_fbd2fbsmodule_h

#include <Python.h>

    PyObject * ALOS_fbd2fbs_C(PyObject *, PyObject *);
    PyObject * setNumberGoodBytes_C(PyObject *, PyObject *);
    PyObject * setNumberBytesPerLine_C(PyObject *, PyObject *);
    PyObject * setNumberLines_C(PyObject *, PyObject *);
    PyObject * setFirstSample_C(PyObject *, PyObject *);
    PyObject * setInPhaseValue_C(PyObject *, PyObject *);
    PyObject * setQuadratureValue_C(PyObject *, PyObject *);
    PyObject * setInputFilename_C(PyObject* self, PyObject* args);
    PyObject * setOutputFilename_C(PyObject* self, PyObject* args);


static PyMethodDef ALOS_fbd2fbs_methods[] =
{
    {"ALOS_fbd2fbs_Py", ALOS_fbd2fbs_C, METH_VARARGS, " "},
    {"setNumberGoodBytes_Py", setNumberGoodBytes_C, METH_VARARGS, " "},
    {"setNumberBytesPerLine_Py", setNumberBytesPerLine_C, METH_VARARGS,
        " "},
    {"setNumberLines_Py", setNumberLines_C, METH_VARARGS, " "},
    {"setFirstSample_Py", setFirstSample_C, METH_VARARGS, " "},
    {"setInPhaseValue_Py", setInPhaseValue_C, METH_VARARGS, " "},
    {"setQuadratureValue_Py", setQuadratureValue_C, METH_VARARGS, " "},
    {"setInputFilename_Py",setInputFilename_C, METH_VARARGS, " "},
    {"setOutputFilename_Py",setOutputFilename_C, METH_VARARGS, " "},
    {NULL, NULL, 0, NULL}
};
#endif
// end of file
