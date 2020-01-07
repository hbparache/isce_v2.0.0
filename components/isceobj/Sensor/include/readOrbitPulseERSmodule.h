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





#ifndef readOrbitPulseERSmodule_h
#define readOrbitPulseERSmodule_h

#include <Python.h>
#include <stdint.h>
#include "readOrbitPulseERSmoduleFortTrans.h"

extern "C"
{
	void readOrbitPulseERS_f();
	PyObject * readOrbitPulseERS_C(PyObject *, PyObject *);
	void setEncodedBinaryTimeCode_f(uint64_t *);
	PyObject * setEncodedBinaryTimeCode_C(PyObject *, PyObject *);
	void setWidth_f(int *);
	PyObject * setWidth_C(PyObject *, PyObject *);
	void setICUoffset_f(int *);
	PyObject * setICUoffset_C(PyObject *, PyObject *);
	void setNumberLines_f(int *);
	PyObject * setNumberLines_C(PyObject *, PyObject *);
	void setSatelliteUTC_f(double *);
	PyObject * setSatelliteUTC_C(PyObject *, PyObject *);
	void setPRF_f(double *);
	PyObject * setPRF_C(PyObject *, PyObject *);
	void setDeltaClock_f(double *);
	PyObject * setDeltaClock_C(PyObject *, PyObject *);
	void getStartingTime_f(double *);
	PyObject * getStartingTime_C(PyObject *, PyObject *);

}

static char * moduleDoc = "module for readOrbitPulseERS.F";

static PyMethodDef readOrbitPulseERS_methods[] =
{
	{"readOrbitPulseERS_Py", readOrbitPulseERS_C, METH_VARARGS, " "},
	{"setEncodedBinaryTimeCode_Py", setEncodedBinaryTimeCode_C, METH_VARARGS, " "},
	{"setWidth_Py", setWidth_C, METH_VARARGS, " "},
	{"setICUoffset_Py", setICUoffset_C, METH_VARARGS, " "},
	{"setNumberLines_Py", setNumberLines_C, METH_VARARGS, " "},
	{"setSatelliteUTC_Py", setSatelliteUTC_C, METH_VARARGS, " "},
	{"setPRF_Py", setPRF_C, METH_VARARGS, " "},
	{"setDeltaClock_Py", setDeltaClock_C, METH_VARARGS, " "},
	{"getStartingTime_Py", getStartingTime_C, METH_VARARGS, " "},
	{NULL, NULL, 0, NULL}
};
#endif readOrbitPulseERSmodule_h
