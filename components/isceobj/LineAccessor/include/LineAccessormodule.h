//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Copyright: 2009 to the present, California Institute of Technology.
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




#ifndef LineAccessormodule_h
#define LineAccessormodule_h

#include <Python.h>

extern "C"
{
    PyObject * getLineAccessorObject_C(PyObject *, PyObject *);
    PyObject * getMachineEndianness_C(PyObject *, PyObject *);
    PyObject * finalizeLineAccessor_C(PyObject *, PyObject *);
    PyObject * initLineAccessor_C(PyObject *, PyObject *);
    PyObject * changeBandScheme_C(PyObject *, PyObject *);
    PyObject * convertFileEndianness_C(PyObject *, PyObject *);
    PyObject * getFileLength_C(PyObject *, PyObject *);
    PyObject * getFileWidth_C(PyObject *, PyObject *);
    PyObject * createFile_C(PyObject *, PyObject *);
    PyObject * rewindImage_C(PyObject *, PyObject *);
    PyObject * getTypeSize_C(PyObject *, PyObject *);
    PyObject * printObjectInfo_C(PyObject *, PyObject *);
    PyObject * printAvailableDataTypesAndSizes_C(PyObject *, PyObject *);
}

BandSchemeType convertIntToBandSchemeType(int band);

static PyMethodDef LineAccessor_methods[] =
{
    {"getLineAccessorObject", getLineAccessorObject_C, METH_VARARGS, " "},
    {"getMachineEndianness", getMachineEndianness_C, METH_VARARGS, " "},
    {"finalizeLineAccessor", finalizeLineAccessor_C, METH_VARARGS, " "},
    {"initLineAccessor", initLineAccessor_C, METH_VARARGS, " "},
    {"changeBandScheme", changeBandScheme_C, METH_VARARGS, " "},
    {"convertFileEndianness", convertFileEndianness_C, METH_VARARGS, " "},
    {"getFileLength", getFileLength_C, METH_VARARGS, " "},
    {"getFileWidth", getFileWidth_C, METH_VARARGS, " "},
    {"createFile", createFile_C, METH_VARARGS, " "},
    {"rewindImage", rewindImage_C, METH_VARARGS, " "},
    {"getTypeSize", getTypeSize_C, METH_VARARGS, " "},
    {"printObjectInfo", printObjectInfo_C, METH_VARARGS, " "},
    {"printAvailableDataTypesAndSizes", printAvailableDataTypesAndSizes_C,
        METH_VARARGS, " "},
    {NULL, NULL, 0, NULL}
};
#endif
// end of file

