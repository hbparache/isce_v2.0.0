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




#ifndef mocompTSXmodule_h
#define mocompTSXmodule_h

#include <Python.h>
#include <stdint.h>
#include "mocompTSXmoduleFortTrans.h"

extern "C"
{
    void mocompTSX_f(uint64_t *,uint64_t *);
    PyObject * mocompTSX_C(PyObject *, PyObject *);
    void setStdWriter_f(uint64_t *);
    PyObject * setStdWriter_C(PyObject *, PyObject *);
    void setNumberRangeBins_f(int *);
    PyObject * setNumberRangeBins_C(PyObject *, PyObject *);
    void setNumberAzLines_f(int *);
    PyObject * setNumberAzLines_C(PyObject *, PyObject *);
    void setDopplerCentroidCoefficients_f(double *, int *);
    void allocate_dopplerCentroidCoefficients_f(int *);
    void deallocate_dopplerCentroidCoefficients_f();
    PyObject * allocate_dopplerCentroidCoefficients_C(PyObject *, PyObject *);
    PyObject * deallocate_dopplerCentroidCoefficients_C(PyObject *, PyObject *);
    PyObject * setDopplerCentroidCoefficients_C(PyObject *, PyObject *);
    void setTime_f(double *, int *);
    void allocate_time_f(int *);
    void deallocate_time_f();
    PyObject * allocate_time_C(PyObject *, PyObject *);
    PyObject * deallocate_time_C(PyObject *, PyObject *);
    PyObject * setTime_C(PyObject *, PyObject *);
    void setPosition_f(double *, int *, int *);
    void allocate_sch_f(int *,int *);
    void deallocate_sch_f();
    PyObject * allocate_sch_C(PyObject *, PyObject *);
    PyObject * deallocate_sch_C(PyObject *, PyObject *);
    PyObject * setPosition_C(PyObject *, PyObject *);
    void setPlanetLocalRadius_f(double *);
    PyObject * setPlanetLocalRadius_C(PyObject *, PyObject *);
    void setBodyFixedVelocity_f(double *);
    PyObject * setBodyFixedVelocity_C(PyObject *, PyObject *);
    void setSpacecraftHeight_f(double *);
    PyObject * setSpacecraftHeight_C(PyObject *, PyObject *);
    void setPRF_f(double *);
    PyObject * setPRF_C(PyObject *, PyObject *);
    void setRangeSamplingRate_f(double *);
    PyObject * setRangeSamplingRate_C(PyObject *, PyObject *);
    void setRadarWavelength_f(double *);
    PyObject * setRadarWavelength_C(PyObject *, PyObject *);
    void setRangeFisrtSample_f(double *);
    PyObject * setRangeFisrtSample_C(PyObject *, PyObject *);
    void getMocompIndex_f(double *, int *);
    PyObject * getMocompIndex_C(PyObject *, PyObject *);
    void getMocompPosition_f(double *, int *, int *);
    PyObject * getMocompPosition_C(PyObject *, PyObject *);
    void getMocompPositionSize_f(int *);
    PyObject * getMocompPositionSize_C(PyObject *, PyObject *);
    void setLookSide_f(int *);
    PyObject * setLookSide_C(PyObject *, PyObject *);
    void getStartingRange_f(double *);
    PyObject* getStartingRange_C(PyObject *, PyObject *);
}

static PyMethodDef mocompTSX_methods[] =
{
    {"mocompTSX_Py", mocompTSX_C, METH_VARARGS, " "},
    {"setStdWriter_Py", setStdWriter_C, METH_VARARGS, " "},
    {"setNumberRangeBins_Py", setNumberRangeBins_C, METH_VARARGS, " "},
    {"setNumberAzLines_Py", setNumberAzLines_C, METH_VARARGS, " "},
    {"allocate_dopplerCentroidCoefficients_Py",
        allocate_dopplerCentroidCoefficients_C, METH_VARARGS, " "},
    {"deallocate_dopplerCentroidCoefficients_Py",
        deallocate_dopplerCentroidCoefficients_C, METH_VARARGS, " "},
    {"setDopplerCentroidCoefficients_Py", setDopplerCentroidCoefficients_C,
        METH_VARARGS, " "},
    {"allocate_time_Py", allocate_time_C, METH_VARARGS, " "},
    {"deallocate_time_Py", deallocate_time_C, METH_VARARGS, " "},
    {"setTime_Py", setTime_C, METH_VARARGS, " "},
    {"allocate_sch_Py", allocate_sch_C, METH_VARARGS, " "},
    {"deallocate_sch_Py", deallocate_sch_C, METH_VARARGS, " "},
    {"setPosition_Py", setPosition_C, METH_VARARGS, " "},
    {"setPlanetLocalRadius_Py", setPlanetLocalRadius_C, METH_VARARGS, " "},
    {"setBodyFixedVelocity_Py", setBodyFixedVelocity_C, METH_VARARGS, " "},
    {"setSpacecraftHeight_Py", setSpacecraftHeight_C, METH_VARARGS, " "},
    {"setPRF_Py", setPRF_C, METH_VARARGS, " "},
    {"setRangeSamplingRate_Py", setRangeSamplingRate_C, METH_VARARGS, " "},
    {"setRadarWavelength_Py", setRadarWavelength_C, METH_VARARGS, " "},
    {"setRangeFisrtSample_Py", setRangeFisrtSample_C, METH_VARARGS, " "},
    {"getMocompIndex_Py", getMocompIndex_C, METH_VARARGS, " "},
    {"getMocompPosition_Py", getMocompPosition_C, METH_VARARGS, " "},
    {"getMocompPositionSize_Py", getMocompPositionSize_C, METH_VARARGS, " "},
    {"setLookSide_Py", setLookSide_C, METH_VARARGS, " "},
    {"getStartingRange_Py", getStartingRange_C, METH_VARARGS, " "},
    {NULL, NULL, 0, NULL}
};
#endif
// end of file
