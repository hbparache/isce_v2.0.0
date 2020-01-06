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





#ifndef DataAccessormodule_h
#define DataAccessormodule_h

#include <Python.h>

extern "C"
{

	PyObject * createAccessor_C(PyObject *, PyObject *);
    PyObject * finalizeAccessor_C(PyObject *, PyObject *);
    PyObject * getFileLength_C(PyObject *, PyObject *);
	PyObject * createFile_C(PyObject *, PyObject *);
	PyObject * getTypeSize_C(PyObject *, PyObject *);
    PyObject * rewind_C(PyObject* self, PyObject* args); 
}


static PyMethodDef DataAccessor_methods[] =
{
	{"createAccessor", createAccessor_C, METH_VARARGS, " "},
	{"finalizeAccessor", finalizeAccessor_C, METH_VARARGS, " "},
	{"getFileLength", getFileLength_C, METH_VARARGS, " "},
	{"createFile", createFile_C, METH_VARARGS, " "},
	{"rewind", rewind_C, METH_VARARGS, " "},
	{"getTypeSize", getTypeSize_C, METH_VARARGS, " "},
    {NULL, NULL, 0, NULL}
};
#endif DataAccessormodule_h
