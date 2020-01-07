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




#ifndef Filtermodule_h
#define Filtermodule_h

#include <Python.h>

extern "C"
{
    PyObject * createFilter_C(PyObject *, PyObject *);
    PyObject * selectBand_C(PyObject *, PyObject *);
    PyObject * setStartLine_C(PyObject *, PyObject *);
    PyObject * setEndLine_C(PyObject *, PyObject *);
    PyObject * finalize_C(PyObject *, PyObject *);
    PyObject * init_C(PyObject *, PyObject *);
    PyObject * extract_C(PyObject *, PyObject *);
}


static PyMethodDef Filter_methods[] =
{
    {"createFilter", createFilter_C, METH_VARARGS, " "},
    {"selectBand", selectBand_C, METH_VARARGS, " "},
    {"setStartLine", setStartLine_C, METH_VARARGS, " "},
    {"setEndLine", setEndLine_C, METH_VARARGS, " "},
    {"extract", extract_C, METH_VARARGS, " "},
    {"finalize", finalize_C, METH_VARARGS, " "},
    {"init", init_C, METH_VARARGS, " "},
    {NULL, NULL, 0, NULL}
};
#endif
// end of file

