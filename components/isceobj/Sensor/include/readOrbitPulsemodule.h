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





#ifndef readOrbitPulsemodule_h
#define readOrbitPulsemodule_h

#include <Python.h>
#include <stdint.h>
#include "readOrbitPulsemoduleFortTrans.h"

extern "C"
{
	void readOrbitPulse_f(uint64_t *,uint64_t *,uint64_t *);
	PyObject * readOrbitPulse_C(PyObject *, PyObject *);
	void setNumberBitesPerLine_f(int *);
	PyObject * setNumberBitesPerLine_C(PyObject *, PyObject *);
	void setNumberLines_f(int *);
	PyObject * setNumberLines_C(PyObject *, PyObject *);

}

static PyMethodDef readOrbitPulse_methods[] =
{
	{"readOrbitPulse_Py", readOrbitPulse_C, METH_VARARGS, " "},
	{"setNumberBitesPerLine_Py", setNumberBitesPerLine_C, METH_VARARGS, " "},
	{"setNumberLines_Py", setNumberLines_C, METH_VARARGS, " "},
	{NULL, NULL, 0, NULL}
};
#endif readOrbitPulsemodule_h
