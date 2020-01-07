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





#ifndef StdOELmodule_h
#define StdOELmodule_h

#include <Python.h>

extern "C"
{

	PyObject * createWriters_C(PyObject *, PyObject *);
	PyObject * finalize_C(PyObject *, PyObject *);
	PyObject * init_C(PyObject *, PyObject *);
	PyObject * setFilename_C(PyObject *, PyObject *);
	PyObject * setFileTag_C(PyObject *, PyObject *);
	PyObject * setTimeStampFlag_C(PyObject *, PyObject *);
}

static PyMethodDef StdOEL_methods[] =
{
	{"createWriters", createWriters_C, METH_VARARGS, " "},
	{"finalize",finalize_C, METH_VARARGS, " "},
	{"init", init_C, METH_VARARGS, " "},
	{"setFilename", setFilename_C, METH_VARARGS, " "},
	{"setFileTag", setFileTag_C, METH_VARARGS, " "},
	{"setTimeStampFlag", setTimeStampFlag_C, METH_VARARGS, " "},
    {NULL, NULL, 0, NULL}
};
#endif StdOELmodule_h
