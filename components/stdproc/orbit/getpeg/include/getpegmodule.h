//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Copyright: 2013 to the present, California Institute of Technology.
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
// Authors: Piyush Agram, Giangi Sacco
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





#ifndef getpegmodule_h
#define getpegmodule_h

#include <Python.h>
#include <stdint.h>
#include "getpegmoduleFortTrans.h"

extern "C"
{
    void getpeg_f();
    PyObject * getpeg_C(PyObject *, PyObject *);
    void setPosition_f(double *, int *, int *);
    void allocate_xyz_f(int *,int *);
    void deallocate_xyz_f();
    PyObject * allocate_xyz_C(PyObject *, PyObject *);
    PyObject * deallocate_xyz_C(PyObject *, PyObject *);
    PyObject * setPosition_C(PyObject *, PyObject *);
    void setVelocity_f(double *, int *, int *);
    void allocate_vxyz_f(int *,int *);
    void deallocate_vxyz_f();
    PyObject * allocate_vxyz_C(PyObject *, PyObject *);
    PyObject * deallocate_vxyz_C(PyObject *, PyObject *);
    PyObject * setVelocity_C(PyObject *, PyObject *);
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
    void getAverageHeight_f(double *);
    PyObject * getAverageHeight_C(PyObject *, PyObject *);
    void getProcVelocity_f(double *);
    PyObject * getProcVelocity_C(PyObject *, PyObject *);

}

static PyMethodDef getpeg_methods[] =
{
    {"getpeg_Py", getpeg_C, METH_VARARGS, " "},
    {"allocate_xyz_Py", allocate_xyz_C, METH_VARARGS, " "},
    {"deallocate_xyz_Py", deallocate_xyz_C, METH_VARARGS, " "},
    {"setPosition_Py", setPosition_C, METH_VARARGS, " "},
    {"allocate_vxyz_Py", allocate_vxyz_C, METH_VARARGS, " "},
    {"deallocate_vxyz_Py", deallocate_vxyz_C, METH_VARARGS, " "},
    {"setVelocity_Py", setVelocity_C, METH_VARARGS, " "},
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
    {"getAverageHeight_Py", getAverageHeight_C, METH_VARARGS, " "},
    {"getProcVelocity_Py", getProcVelocity_C, METH_VARARGS, " "},
    {NULL, NULL, 0, NULL}
};
#endif

// end of file
