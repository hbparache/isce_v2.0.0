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




#ifndef sch2orbitmodule_h
#define sch2orbitmodule_h

#include <Python.h>
#include <stdint.h>
#include "sch2orbitmoduleFortTrans.h"

extern "C"
{
    void setStdWriter_f(uint64_t *);
    PyObject * setStdWriter_C(PyObject *, PyObject *);
    void sch2orbit_f();
    PyObject * sch2orbit_C(PyObject *, PyObject *);
    void setOrbitPosition_f(double *, int *);
    void allocateArrays_f(int *);
    PyObject * allocateArrays_C(PyObject *, PyObject *);
    void deallocateArrays_f();
    PyObject * deallocateArrays_C(PyObject*, PyObject*);
    PyObject * setOrbitPosition_C(PyObject *, PyObject *);
    void setOrbitVelocity_f(double *, int *);
    PyObject * setOrbitVelocity_C(PyObject *, PyObject *);
    void setPlanetGM_f(double *);
    PyObject * setPlanetGM_C(PyObject *, PyObject *);
    void setEllipsoidMajorSemiAxis_f(double *);
    PyObject * setEllipsoidMajorSemiAxis_C(PyObject *, PyObject *);
    void setEllipsoidEccentricitySquared_f(double *);
    PyObject * setEllipsoidEccentricitySquared_C(PyObject *, PyObject *);
    void setPegLatitude_f(double *);
    PyObject * setPegLatitude_C(PyObject *, PyObject *);
    void setPegLongitude_f(double *);
    PyObject * setPegLongitude_C(PyObject *, PyObject *);
    void setPegHeading_f(double *);
    PyObject * setPegHeading_C(PyObject *, PyObject *);
    void setRadiusOfCurvature_f(double *);
    PyObject * setRadiusOfCurvature_C(PyObject *, PyObject *);
    void getXYZPosition_f(double *, int *);
    PyObject * getXYZPosition_C(PyObject *, PyObject *);
    void getXYZVelocity_f(double *, int *);
    PyObject * getXYZVelocity_C(PyObject *, PyObject *);
    void getXYZGravitationalAcceleration_f(double *, int *);
    PyObject * getXYZGravitationalAcceleration_C(PyObject *, PyObject *);

}

static PyMethodDef sch2orbit_methods[] =
{
    {"setStdWriter_Py", setStdWriter_C, METH_VARARGS, " "},
    {"sch2orbit_Py", sch2orbit_C, METH_VARARGS, " "},
    {"allocateArrays_Py", allocateArrays_C, METH_VARARGS, " "},
    {"deallocateArrays_Py", deallocateArrays_C, METH_VARARGS, " "},
    {"setOrbitPosition_Py", setOrbitPosition_C, METH_VARARGS, " "},
    {"setOrbitVelocity_Py", setOrbitVelocity_C, METH_VARARGS, " "},
    {"setPlanetGM_Py", setPlanetGM_C, METH_VARARGS, " "},
    {"setEllipsoidMajorSemiAxis_Py", setEllipsoidMajorSemiAxis_C, METH_VARARGS,
        " "},
    {"setEllipsoidEccentricitySquared_Py", setEllipsoidEccentricitySquared_C,
        METH_VARARGS, " "},
    {"setPegLatitude_Py", setPegLatitude_C, METH_VARARGS, " "},
    {"setPegLongitude_Py", setPegLongitude_C, METH_VARARGS, " "},
    {"setPegHeading_Py", setPegHeading_C, METH_VARARGS, " "},
    {"setRadiusOfCurvature_Py", setRadiusOfCurvature_C, METH_VARARGS, " "},
    {"getXYZPosition_Py", getXYZPosition_C, METH_VARARGS, " "},
    {"getXYZVelocity_Py", getXYZVelocity_C, METH_VARARGS, " "},
    {"getXYZGravitationalAcceleration_Py", getXYZGravitationalAcceleration_C,
        METH_VARARGS, " "},
    {NULL, NULL, 0, NULL}
};
#endif sch2orbitmodule_h
