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




#ifndef setmocomppathmodule_h
#define setmocomppathmodule_h

#include <Python.h>
#include <stdint.h>
#include "setmocomppathmoduleFortTrans.h"

extern "C"
{
    void setmocomppath_f();
    PyObject * setmocomppath_C(PyObject *, PyObject *);
    void setFirstPosition_f(double *, int *, int *);
    void allocate_xyz1_f(int *,int *);
    void deallocate_xyz1_f();
    PyObject * allocate_xyz1_C(PyObject *, PyObject *);
    PyObject * deallocate_xyz1_C(PyObject *, PyObject *);
    PyObject * setFirstPosition_C(PyObject *, PyObject *);
    void setFirstVelocity_f(double *, int *, int *);
    void allocate_vxyz1_f(int *,int *);
    void deallocate_vxyz1_f();
    PyObject * allocate_vxyz1_C(PyObject *, PyObject *);
    PyObject * deallocate_vxyz1_C(PyObject *, PyObject *);
    PyObject * setFirstVelocity_C(PyObject *, PyObject *);
    void setSecondPosition_f(double *, int *, int *);
    void allocate_xyz2_f(int *,int *);
    void deallocate_xyz2_f();
    PyObject * allocate_xyz2_C(PyObject *, PyObject *);
    PyObject * deallocate_xyz2_C(PyObject *, PyObject *);
    PyObject * setSecondPosition_C(PyObject *, PyObject *);
    void setSecondVelocity_f(double *, int *, int *);
    void allocate_vxyz2_f(int *,int *);
    void deallocate_vxyz2_f();
    PyObject * allocate_vxyz2_C(PyObject *, PyObject *);
    PyObject * deallocate_vxyz2_C(PyObject *, PyObject *);
    PyObject * setSecondVelocity_C(PyObject *, PyObject *);
    void setStdWriter_f(uint64_t *);
    PyObject * setStdWriter_C(PyObject *, PyObject *);
    void setPlanetGM_f(double *);
    PyObject * setPlanetGM_C(PyObject *, PyObject *);
    void setEllipsoidMajorSemiAxis_f(double *);
    PyObject * setEllipsoidMajorSemiAxis_C(PyObject *, PyObject *);
    void setEllipsoidEccentricitySquared_f(double *);
    PyObject * setEllipsoidEccentricitySquared_C(PyObject *, PyObject *);
    void getPegLatitude_f(double *);
    PyObject * getPegLatitude_C(PyObject *, PyObject *);
    void getPegLongitude_f(double *);
    PyObject * getPegLongitude_C(PyObject *, PyObject *);
    void getPegHeading_f(double *);
    PyObject * getPegHeading_C(PyObject *, PyObject *);
    void getPegRadiusOfCurvature_f(double *);
    PyObject * getPegRadiusOfCurvature_C(PyObject *, PyObject *);
    void getFirstAverageHeight_f(double *);
    PyObject * getFirstAverageHeight_C(PyObject *, PyObject *);
    void getSecondAverageHeight_f(double *);
    PyObject * getSecondAverageHeight_C(PyObject *, PyObject *);
    void getFirstProcVelocity_f(double *);
    PyObject * getFirstProcVelocity_C(PyObject *, PyObject *);
    void getSecondProcVelocity_f(double *);
    PyObject * getSecondProcVelocity_C(PyObject *, PyObject *);

}

static PyMethodDef setmocomppath_methods[] =
{
    {"setmocomppath_Py", setmocomppath_C, METH_VARARGS, " "},
    {"allocate_xyz1_Py", allocate_xyz1_C, METH_VARARGS, " "},
    {"deallocate_xyz1_Py", deallocate_xyz1_C, METH_VARARGS, " "},
    {"setFirstPosition_Py", setFirstPosition_C, METH_VARARGS, " "},
    {"allocate_vxyz1_Py", allocate_vxyz1_C, METH_VARARGS, " "},
    {"deallocate_vxyz1_Py", deallocate_vxyz1_C, METH_VARARGS, " "},
    {"setFirstVelocity_Py", setFirstVelocity_C, METH_VARARGS, " "},
    {"allocate_xyz2_Py", allocate_xyz2_C, METH_VARARGS, " "},
    {"deallocate_xyz2_Py", deallocate_xyz2_C, METH_VARARGS, " "},
    {"setSecondPosition_Py", setSecondPosition_C, METH_VARARGS, " "},
    {"allocate_vxyz2_Py", allocate_vxyz2_C, METH_VARARGS, " "},
    {"deallocate_vxyz2_Py", deallocate_vxyz2_C, METH_VARARGS, " "},
    {"setSecondVelocity_Py", setSecondVelocity_C, METH_VARARGS, " "},
    {"setStdWriter_Py", setStdWriter_C, METH_VARARGS, " "},
    {"setPlanetGM_Py", setPlanetGM_C, METH_VARARGS, " "},
    {"setEllipsoidMajorSemiAxis_Py", setEllipsoidMajorSemiAxis_C, METH_VARARGS,
        " "},
    {"setEllipsoidEccentricitySquared_Py", setEllipsoidEccentricitySquared_C,
        METH_VARARGS, " "},
    {"getPegLatitude_Py", getPegLatitude_C, METH_VARARGS, " "},
    {"getPegLongitude_Py", getPegLongitude_C, METH_VARARGS, " "},
    {"getPegHeading_Py", getPegHeading_C, METH_VARARGS, " "},
    {"getPegRadiusOfCurvature_Py", getPegRadiusOfCurvature_C, METH_VARARGS,
        " "},
    {"getFirstAverageHeight_Py", getFirstAverageHeight_C, METH_VARARGS, " "},
    {"getSecondAverageHeight_Py", getSecondAverageHeight_C, METH_VARARGS, " "},
    {"getFirstProcVelocity_Py", getFirstProcVelocity_C, METH_VARARGS, " "},
    {"getSecondProcVelocity_Py", getSecondProcVelocity_C, METH_VARARGS, " "},
    {NULL, NULL, 0, NULL}
};
#endif

// end of file
