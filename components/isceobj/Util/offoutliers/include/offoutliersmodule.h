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





#ifndef offoutliersmodule_h
#define offoutliersmodule_h

#include <Python.h>
#include <stdint.h>
#include "offoutliersmoduleFortTrans.h"

extern "C"
{
    void setStdWriter_f(uint64_t *);
    PyObject * setStdWriter_C(PyObject *, PyObject *);
	void offoutliers_f();
	PyObject * offoutliers_C(PyObject *, PyObject *);
	void getIndexArray_f(int *, int *);
	void allocate_indexArray_f(int *);
	void deallocate_indexArray_f();
	PyObject * allocate_indexArray_C(PyObject *, PyObject *);
	PyObject * deallocate_indexArray_C(PyObject *, PyObject *);
	PyObject * getIndexArray_C(PyObject *, PyObject *);
	void getIndexArraySize_f(int *);
	PyObject * getIndexArraySize_C(PyObject *, PyObject *);
	void getAverageOffsetDown_f(float *);
	PyObject * getAverageOffsetDown_C(PyObject *, PyObject *);
	void getAverageOffsetAcross_f(float *);
	PyObject * getAverageOffsetAcross_C(PyObject *, PyObject *);
	void setNumberOfPoints_f(int *);
	PyObject * setNumberOfPoints_C(PyObject *, PyObject *);
	void setLocationAcross_f(double *, int *);
	void allocate_xd_f(int *);
	void deallocate_xd_f();
	PyObject * allocate_xd_C(PyObject *, PyObject *);
	PyObject * deallocate_xd_C(PyObject *, PyObject *);
	PyObject * setLocationAcross_C(PyObject *, PyObject *);
	void setLocationAcrossOffset_f(double *, int *);
	void allocate_acshift_f(int *);
	void deallocate_acshift_f();
	PyObject * allocate_acshift_C(PyObject *, PyObject *);
	PyObject * deallocate_acshift_C(PyObject *, PyObject *);
	PyObject * setLocationAcrossOffset_C(PyObject *, PyObject *);
	void setLocationDown_f(double *, int *);
	void allocate_yd_f(int *);
	void deallocate_yd_f();
	PyObject * allocate_yd_C(PyObject *, PyObject *);
	PyObject * deallocate_yd_C(PyObject *, PyObject *);
	PyObject * setLocationDown_C(PyObject *, PyObject *);
	void setLocationDownOffset_f(double *, int *);
	void allocate_dnshift_f(int *);
	void deallocate_dnshift_f();
	PyObject * allocate_dnshift_C(PyObject *, PyObject *);
	PyObject * deallocate_dnshift_C(PyObject *, PyObject *);
	PyObject * setLocationDownOffset_C(PyObject *, PyObject *);
	void setDistance_f(float *);
	PyObject * setDistance_C(PyObject *, PyObject *);
	void setSign_f(double *, int *);
	void allocate_sig_f(int *);
	void deallocate_sig_f();
	PyObject * allocate_sig_C(PyObject *, PyObject *);
	PyObject * deallocate_sig_C(PyObject *, PyObject *);
	PyObject * setSign_C(PyObject *, PyObject *);
	void setSNR_f(double *, int *);
	void allocate_s_f(int *);
	void deallocate_s_f();
	PyObject * allocate_s_C(PyObject *, PyObject *);
	PyObject * deallocate_s_C(PyObject *, PyObject *);
	PyObject * setSNR_C(PyObject *, PyObject *);

}

static PyMethodDef offoutliers_methods[] =
{
    {"setStdWriter_Py", setStdWriter_C, METH_VARARGS, " "},
	{"offoutliers_Py", offoutliers_C, METH_VARARGS, " "},
	{"allocate_indexArray_Py", allocate_indexArray_C, METH_VARARGS, " "},
	{"deallocate_indexArray_Py", deallocate_indexArray_C, METH_VARARGS, " "},
	{"getIndexArray_Py", getIndexArray_C, METH_VARARGS, " "},
	{"getIndexArraySize_Py", getIndexArraySize_C, METH_VARARGS, " "},
	{"getAverageOffsetDown_Py", getAverageOffsetDown_C, METH_VARARGS, " "},
	{"getAverageOffsetAcross_Py", getAverageOffsetAcross_C, METH_VARARGS, " "},
	{"setNumberOfPoints_Py", setNumberOfPoints_C, METH_VARARGS, " "},
	{"allocate_xd_Py", allocate_xd_C, METH_VARARGS, " "},
	{"deallocate_xd_Py", deallocate_xd_C, METH_VARARGS, " "},
	{"setLocationAcross_Py", setLocationAcross_C, METH_VARARGS, " "},
	{"allocate_acshift_Py", allocate_acshift_C, METH_VARARGS, " "},
	{"deallocate_acshift_Py", deallocate_acshift_C, METH_VARARGS, " "},
	{"setLocationAcrossOffset_Py", setLocationAcrossOffset_C, METH_VARARGS, " "},
	{"allocate_yd_Py", allocate_yd_C, METH_VARARGS, " "},
	{"deallocate_yd_Py", deallocate_yd_C, METH_VARARGS, " "},
	{"setLocationDown_Py", setLocationDown_C, METH_VARARGS, " "},
	{"allocate_dnshift_Py", allocate_dnshift_C, METH_VARARGS, " "},
	{"deallocate_dnshift_Py", deallocate_dnshift_C, METH_VARARGS, " "},
	{"setLocationDownOffset_Py", setLocationDownOffset_C, METH_VARARGS, " "},
	{"setDistance_Py", setDistance_C, METH_VARARGS, " "},
	{"allocate_sig_Py", allocate_sig_C, METH_VARARGS, " "},
	{"deallocate_sig_Py", deallocate_sig_C, METH_VARARGS, " "},
	{"setSign_Py", setSign_C, METH_VARARGS, " "},
	{"allocate_s_Py", allocate_s_C, METH_VARARGS, " "},
	{"deallocate_s_Py", deallocate_s_C, METH_VARARGS, " "},
	{"setSNR_Py", setSNR_C, METH_VARARGS, " "},
	{NULL, NULL, 0, NULL}
};
#endif offoutliersmodule_h
