//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                  Giangi Sacco
//                        NASA Jet Propulsion Laboratory
//                      California Institute of Technology
//                        (C) 2009  All Rights Reserved
//
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#ifndef formslcmodule_h
#define formslcmodule_h

#include "LineAccessor.h"
#include "formslcmoduleFortTrans.h"
#include <stdint.h>

extern "C"
{
	void formslc_f(uint64_t *, uint64_t *);
	PyObject * formslc_C(PyObject *, PyObject *);
	void setNumberGoodBytes_f(int *);
	PyObject * setNumberGoodBytes_C(PyObject *, PyObject *);
	void setNumberBytesPerLine_f(int *);
	PyObject * setNumberBytesPerLine_C(PyObject *, PyObject *);
	void setDebugFlag_f(int *);
	PyObject * setDebugFlag_C(PyObject *, PyObject *);
	void setDeskewFlag_f(char *, int *);
	PyObject * setDeskewFlag_C(PyObject *, PyObject *);
	void setSecondaryRangeMigrationFlag_f(char *, int *);
	PyObject * setSecondaryRangeMigrationFlag_C(PyObject *, PyObject *);
	void setFirstLine_f(int *);
	PyObject * setFirstLine_C(PyObject *, PyObject *);
	void setNumberPatches_f(int *);
	PyObject * setNumberPatches_C(PyObject *, PyObject *);
	void setFirstSample_f(int *);
	PyObject * setFirstSample_C(PyObject *, PyObject *);
	void setAzimuthPatchSize_f(int *);
	PyObject * setAzimuthPatchSize_C(PyObject *, PyObject *);
	void setNumberValidPulses_f(int *);
	PyObject * setNumberValidPulses_C(PyObject *, PyObject *);
	void setCaltoneLocation_f(float *);
	PyObject * setCaltoneLocation_C(PyObject *, PyObject *);
	void setStartRangeBin_f(int *);
	PyObject * setStartRangeBin_C(PyObject *, PyObject *);
	void setNumberRangeBin_f(int *);
	PyObject * setNumberRangeBin_C(PyObject *, PyObject *);
	void setDopplerCentroidCoefficients_f(double *, int *);
	void allocate_dopplerCoefficients_f(int *);
	void deallocate_dopplerCoefficients_f();
	PyObject * allocate_dopplerCoefficients_C(PyObject *, PyObject *);
	PyObject * deallocate_dopplerCoefficients_C(PyObject *, PyObject *);
	PyObject * setDopplerCentroidCoefficients_C(PyObject *, PyObject *);
	void setPlanetRadiusOfCurvature_f(double *);
	PyObject * setPlanetRadiusOfCurvature_C(PyObject *, PyObject *);
	void setBodyFixedVelocity_f(float *);
	PyObject * setBodyFixedVelocity_C(PyObject *, PyObject *);
	void setSpacecraftHeight_f(double *);
	PyObject * setSpacecraftHeight_C(PyObject *, PyObject *);
	void setPlanetGravitationalConstant_f(double *);
	PyObject * setPlanetGravitationalConstant_C(PyObject *, PyObject *);
	void setPointingDirection_f(int *);
	PyObject * setPointingDirection_C(PyObject *, PyObject *);
	void setAntennaSCHVelocity_f(double *, int *);
	void allocate_r_platvel1_f(int *);
	void deallocate_r_platvel1_f();
	PyObject * allocate_r_platvel1_C(PyObject *, PyObject *);
	PyObject * deallocate_r_platvel1_C(PyObject *, PyObject *);
	PyObject * setAntennaSCHVelocity_C(PyObject *, PyObject *);
	void setAntennaSCHAcceleration_f(double *, int *);
	void allocate_r_platacc1_f(int *);
	void deallocate_r_platacc1_f();
	PyObject * allocate_r_platacc1_C(PyObject *, PyObject *);
	PyObject * deallocate_r_platacc1_C(PyObject *, PyObject *);
	PyObject * setAntennaSCHAcceleration_C(PyObject *, PyObject *);
	void setRangeFirstSample_f(double *);
	PyObject * setRangeFirstSample_C(PyObject *, PyObject *);
	void setPRF_f(float *);
	PyObject * setPRF_C(PyObject *, PyObject *);
	void setInPhaseValue_f(float *);
	PyObject * setInPhaseValue_C(PyObject *, PyObject *);
	void setQuadratureValue_f(float *);
	PyObject * setQuadratureValue_C(PyObject *, PyObject *);
	void setIQFlip_f(char *, int *);
	PyObject * setIQFlip_C(PyObject *, PyObject *);
	void setAzimuthResolution_f(float *);
	PyObject * setAzimuthResolution_C(PyObject *, PyObject *);
	void setNumberAzimuthLooks_f(int *);
	PyObject * setNumberAzimuthLooks_C(PyObject *, PyObject *);
	void setRangeSamplingRate_f(float *);
	PyObject * setRangeSamplingRate_C(PyObject *, PyObject *);
	void setChirpSlope_f(float *);
	PyObject * setChirpSlope_C(PyObject *, PyObject *);
	void setRangePulseDuration_f(float *);
	PyObject * setRangePulseDuration_C(PyObject *, PyObject *);
	void setRangeChirpExtensionPoints_f(int *);
	PyObject * setRangeChirpExtensionPoints_C(PyObject *, PyObject *);
	void setRadarWavelength_f(double *);
	PyObject * setRadarWavelength_C(PyObject *, PyObject *);
	void setRangeSpectralWeighting_f(float *);
	PyObject * setRangeSpectralWeighting_C(PyObject *, PyObject *);
	void setSpectralShiftFractions_f(float *, int *);
	void allocate_spectralShiftFrac_f(int *);
	void deallocate_spectralShiftFrac_f();
	PyObject * allocate_spectralShiftFrac_C(PyObject *, PyObject *);
	PyObject * deallocate_spectralShiftFrac_C(PyObject *, PyObject *);
	PyObject * setSpectralShiftFractions_C(PyObject *, PyObject *);
	void setLinearResamplingCoefficiets_f(double *, int *);
	void allocate_linearResampCoeff_f(int *);
	void deallocate_linearResampCoeff_f();
	PyObject * allocate_linearResampCoeff_C(PyObject *, PyObject *);
	PyObject * deallocate_linearResampCoeff_C(PyObject *, PyObject *);
	PyObject * setLinearResamplingCoefficiets_C(PyObject *, PyObject *);
	void setLinearResamplingDeltas_f(double *, int *);
	void allocate_linearResampDeltas_f(int *);
	void deallocate_linearResampDeltas_f();
	PyObject * allocate_linearResampDeltas_C(PyObject *, PyObject *);
	PyObject * deallocate_linearResampDeltas_C(PyObject *, PyObject *);
	PyObject * setLinearResamplingDeltas_C(PyObject *, PyObject *);

}

static PyMethodDef formslc_methods[] =
{
	{"formslc_Py", formslc_C, METH_VARARGS, " "},
	{"setNumberGoodBytes_Py", setNumberGoodBytes_C, METH_VARARGS, " "},
	{"setNumberBytesPerLine_Py", setNumberBytesPerLine_C, METH_VARARGS, " "},
	{"setDebugFlag_Py", setDebugFlag_C, METH_VARARGS, " "},
	{"setDeskewFlag_Py", setDeskewFlag_C, METH_VARARGS, " "},
	{"setSecondaryRangeMigrationFlag_Py", setSecondaryRangeMigrationFlag_C, METH_VARARGS, " "},
	{"setFirstLine_Py", setFirstLine_C, METH_VARARGS, " "},
	{"setNumberPatches_Py", setNumberPatches_C, METH_VARARGS, " "},
	{"setFirstSample_Py", setFirstSample_C, METH_VARARGS, " "},
	{"setAzimuthPatchSize_Py", setAzimuthPatchSize_C, METH_VARARGS, " "},
	{"setNumberValidPulses_Py", setNumberValidPulses_C, METH_VARARGS, " "},
	{"setCaltoneLocation_Py", setCaltoneLocation_C, METH_VARARGS, " "},
	{"setStartRangeBin_Py", setStartRangeBin_C, METH_VARARGS, " "},
	{"setNumberRangeBin_Py", setNumberRangeBin_C, METH_VARARGS, " "},
	{"allocate_dopplerCoefficients_Py", allocate_dopplerCoefficients_C, METH_VARARGS, " "},
	{"deallocate_dopplerCoefficients_Py", deallocate_dopplerCoefficients_C, METH_VARARGS, " "},
	{"setDopplerCentroidCoefficients_Py", setDopplerCentroidCoefficients_C, METH_VARARGS, " "},
	{"setPlanetRadiusOfCurvature_Py", setPlanetRadiusOfCurvature_C, METH_VARARGS, " "},
	{"setBodyFixedVelocity_Py", setBodyFixedVelocity_C, METH_VARARGS, " "},
	{"setSpacecraftHeight_Py", setSpacecraftHeight_C, METH_VARARGS, " "},
	{"setPlanetGravitationalConstant_Py", setPlanetGravitationalConstant_C, METH_VARARGS, " "},
	{"setPointingDirection_Py", setPointingDirection_C, METH_VARARGS, " "},
	{"allocate_r_platvel1_Py", allocate_r_platvel1_C, METH_VARARGS, " "},
	{"deallocate_r_platvel1_Py", deallocate_r_platvel1_C, METH_VARARGS, " "},
	{"setAntennaSCHVelocity_Py", setAntennaSCHVelocity_C, METH_VARARGS, " "},
	{"allocate_r_platacc1_Py", allocate_r_platacc1_C, METH_VARARGS, " "},
	{"deallocate_r_platacc1_Py", deallocate_r_platacc1_C, METH_VARARGS, " "},
	{"setAntennaSCHAcceleration_Py", setAntennaSCHAcceleration_C, METH_VARARGS, " "},
	{"setRangeFirstSample_Py", setRangeFirstSample_C, METH_VARARGS, " "},
	{"setPRF_Py", setPRF_C, METH_VARARGS, " "},
	{"setInPhaseValue_Py", setInPhaseValue_C, METH_VARARGS, " "},
	{"setQuadratureValue_Py", setQuadratureValue_C, METH_VARARGS, " "},
	{"setIQFlip_Py", setIQFlip_C, METH_VARARGS, " "},
	{"setAzimuthResolution_Py", setAzimuthResolution_C, METH_VARARGS, " "},
	{"setNumberAzimuthLooks_Py", setNumberAzimuthLooks_C, METH_VARARGS, " "},
	{"setRangeSamplingRate_Py", setRangeSamplingRate_C, METH_VARARGS, " "},
	{"setChirpSlope_Py", setChirpSlope_C, METH_VARARGS, " "},
	{"setRangePulseDuration_Py", setRangePulseDuration_C, METH_VARARGS, " "},
	{"setRangeChirpExtensionPoints_Py", setRangeChirpExtensionPoints_C, METH_VARARGS, " "},
	{"setRadarWavelength_Py", setRadarWavelength_C, METH_VARARGS, " "},
	{"setRangeSpectralWeighting_Py", setRangeSpectralWeighting_C, METH_VARARGS, " "},
	{"allocate_spectralShiftFrac_Py", allocate_spectralShiftFrac_C, METH_VARARGS, " "},
	{"deallocate_spectralShiftFrac_Py", deallocate_spectralShiftFrac_C, METH_VARARGS, " "},
	{"setSpectralShiftFractions_Py", setSpectralShiftFractions_C, METH_VARARGS, " "},
	{"allocate_linearResampCoeff_Py", allocate_linearResampCoeff_C, METH_VARARGS, " "},
	{"deallocate_linearResampCoeff_Py", deallocate_linearResampCoeff_C, METH_VARARGS, " "},
	{"setLinearResamplingCoefficiets_Py", setLinearResamplingCoefficiets_C, METH_VARARGS, " "},
	{"allocate_linearResampDeltas_Py", allocate_linearResampDeltas_C, METH_VARARGS, " "},
	{"deallocate_linearResampDeltas_Py", deallocate_linearResampDeltas_C, METH_VARARGS, " "},
	{"setLinearResamplingDeltas_Py", setLinearResamplingDeltas_C, METH_VARARGS, " "},
	{NULL, NULL, 0, NULL}
};
#endif formslcmodule_h
