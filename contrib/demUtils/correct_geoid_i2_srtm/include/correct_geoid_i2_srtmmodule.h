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




#ifndef correct_geoid_i2_srtmmodule_h
#define correct_geoid_i2_srtmmodule_h

#include <Python.h>
#include <stdint.h>
#include "correct_geoid_i2_srtmmoduleFortTrans.h"

extern "C"
{
    void correct_geoid_i2_srtm_f(uint64_t *,uint64_t *);
    PyObject * correct_geoid_i2_srtm_C(PyObject *, PyObject *);
    void setWidth_f(int *);
    PyObject * setWidth_C(PyObject *, PyObject *);
    void setStartLatitude_f(double *);
    PyObject * setStartLatitude_C(PyObject *, PyObject *);
    void setStartLongitude_f(double *);
    PyObject * setStartLongitude_C(PyObject *, PyObject *);
    void setDeltaLatitude_f(double *);
    PyObject * setDeltaLatitude_C(PyObject *, PyObject *);
    void setDeltaLongitude_f(double *);
    PyObject * setDeltaLongitude_C(PyObject *, PyObject *);
    void setNumberLines_f(int *);
    PyObject * setNumberLines_C(PyObject *, PyObject *);
    void setConversionType_f(int *);
    PyObject * setConversionType_C(PyObject *, PyObject *);
    void setGeoidFilename_f(char *, int*);
    PyObject * setGeoidFilename_C(PyObject *, PyObject *);
    void setStdWriter_f(uint64_t *);
    PyObject * setStdWriter_C(PyObject *, PyObject *);
}

static PyMethodDef correct_geoid_i2_srtm_methods[] =
{
    {"correct_geoid_i2_srtm_Py", correct_geoid_i2_srtm_C, METH_VARARGS, " "},
    {"setWidth_Py", setWidth_C, METH_VARARGS, " "},
    {"setStartLatitude_Py", setStartLatitude_C, METH_VARARGS, " "},
    {"setStartLongitude_Py", setStartLongitude_C, METH_VARARGS, " "},
    {"setDeltaLatitude_Py", setDeltaLatitude_C, METH_VARARGS, " "},
    {"setDeltaLongitude_Py", setDeltaLongitude_C, METH_VARARGS, " "},
    {"setNumberLines_Py", setNumberLines_C, METH_VARARGS, " "},
    {"setConversionType_Py", setConversionType_C, METH_VARARGS, " "},
    {"setGeoidFilename_Py", setGeoidFilename_C, METH_VARARGS, " "},
    {"setStdWriter_Py", setStdWriter_C, METH_VARARGS, " "},
    {NULL, NULL, 0, NULL}
};
#endif
// end of file
