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





#ifndef cpxmag2rgmodule_h
#define cpxmag2rgmodule_h

#include <Python.h>
#include <stdint.h>
#include "cpxmag2rgmoduleFortTrans.h"

extern "C"
{
    void setStdWriter_f(uint64_t *);
    PyObject * setStdWriter_C(PyObject *, PyObject *);
	void cpxmag2rg_f(uint64_t *,uint64_t *,uint64_t *);
	PyObject * cpxmag2rg_C(PyObject *, PyObject *);
	void setLineLength_f(int *);
	PyObject * setLineLength_C(PyObject *, PyObject *);
	void setFileLength_f(int *);
	PyObject * setFileLength_C(PyObject *, PyObject *);
	void setAcOffset_f(int *);
	PyObject * setAcOffset_C(PyObject *, PyObject *);
	void setDnOffset_f(int *);
	PyObject * setDnOffset_C(PyObject *, PyObject *);

}

static char * moduleDoc = "module for cpxmag2rg.F";

static PyMethodDef cpxmag2rg_methods[] =
{
    {"setStdWriter_Py", setStdWriter_C, METH_VARARGS, " "},
	{"cpxmag2rg_Py", cpxmag2rg_C, METH_VARARGS, " "},
	{"setLineLength_Py", setLineLength_C, METH_VARARGS, " "},
	{"setFileLength_Py", setFileLength_C, METH_VARARGS, " "},
	{"setAcOffset_Py", setAcOffset_C, METH_VARARGS, " "},
	{"setDnOffset_Py", setDnOffset_C, METH_VARARGS, " "},
	{NULL, NULL, 0, NULL}
};
#endif cpxmag2rgmodule_h
