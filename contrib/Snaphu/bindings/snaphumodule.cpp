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




#include <Python.h>
#include "snaphumodule.h"

using namespace std;
infileT infile[1];
outfileT outfile[1];
paramT params[1];

static char * const __doc__ =
    "snaphu module for unwrapping interferograms";

PyModuleDef moduledef = {
    // header
    PyModuleDef_HEAD_INIT,
    // name of the module
    "snaphu",
    // module documentation string
    __doc__,
    // size of the per-interpreter state of the module;
    // -1 if this state is global
    -1,
    snaphu_methods,
};

// initialization function for the module
// *must* be called PyInit_snaphu
PyMODINIT_FUNC
PyInit_snaphu()
{
    // create the module using moduledef struct defined above
    PyObject * module = PyModule_Create(&moduledef);
    // check whether module creation succeeded and raise an exception if not
    if (!module) {
        return module;
    }
    // otherwise, we have an initialized module
    // and return the newly created module
    return module;
}

PyObject *snaphu_C(PyObject *self,PyObject *args)
{
    long linelen;
    if(!PyArg_ParseTuple(args,"l",&linelen))
    {
        return NULL;
    }
    snaphu(infile,outfile,params,linelen);

    return Py_BuildValue("i",0);
}

PyObject *setDefaults_C(PyObject *self,PyObject *args)
{
    SetDefaults(infile,outfile,params);

    return Py_BuildValue("i",0);
}

PyObject *setInput_C(PyObject *self,PyObject *args)
{
    char *inputFile;
    if (!PyArg_ParseTuple(args,"s",&inputFile))
    {
        return NULL;
    }
    StrNCopy(infile->infile,inputFile,MAXSTRLEN);

    return Py_BuildValue("i",0);
}

PyObject *setOutput_C(PyObject *self,PyObject *args)
{
    char *outputFile;
    if(!PyArg_ParseTuple(args,"s",&outputFile))
    {
        return NULL;
    }
    StrNCopy(outfile->outfile,outputFile,MAXSTRLEN);

    return Py_BuildValue("i",0);
}

PyObject *setMagnitude_C(PyObject *self, PyObject *args)
{
    char *magFile;
    if(!PyArg_ParseTuple(args,"s",&magFile))
    {
        return NULL;
    }
    StrNCopy(infile->magfile,magFile,MAXSTRLEN);
    return Py_BuildValue("i",0);
}

PyObject *setConnectedComponents_C(PyObject *self,PyObject *args)
{
    char *outputFile;
    if(!PyArg_ParseTuple(args,"s",&outputFile))
    {
        return NULL;
    }
    StrNCopy(outfile->conncompfile, outputFile, MAXSTRLEN);
    return Py_BuildValue("i",0);
}

PyObject *setCorrfile_C(PyObject *self,PyObject *args)
{
    char *corrFile;
    if(!PyArg_ParseTuple(args,"s", &corrFile))
    {
        return NULL;
    }
    StrNCopy(infile->corrfile, corrFile, MAXSTRLEN);

    return Py_BuildValue("i",0);
}

PyObject *setCostMode_C(PyObject *self,PyObject *args)
{
    int costMode;

    if(!PyArg_ParseTuple(args,"i",&costMode))
    {
        return NULL;
    }
    params->costmode = costMode;

    return Py_BuildValue("i",0);
}

PyObject *setWavelength_C(PyObject *self,PyObject *args)
{
    double wavelength;
    if(!PyArg_ParseTuple(args,"d",&wavelength))
    {
        return NULL;
    }
    params->lambda = wavelength;

    return Py_BuildValue("i",0);
}

PyObject *setAltitude_C(PyObject *self,PyObject *args)
{
    double altitude;
    if(!PyArg_ParseTuple(args,"d",&altitude))
    {
        return NULL;
    }
    params->altitude = altitude;

    return Py_BuildValue("i",0);
}

PyObject *setEarthRadius_C(PyObject *self,PyObject *args)
{
    double radius;
    if(!PyArg_ParseTuple(args,"d",&radius))
    {
        return NULL;
    }
    params->earthradius = radius;

    return Py_BuildValue("i",0);
}

PyObject *setCorrLooks_C(PyObject *self, PyObject *args)
{
    double looks;
    if(!PyArg_ParseTuple(args,"d",&looks))
    {
        return NULL;
    }
    params->ncorrlooks = looks;

    return Py_BuildValue("i", 0);
}

PyObject *setRangeLooks_C(PyObject *self, PyObject *args)
{
    int looks;
    if(!PyArg_ParseTuple(args,"i", &looks))
    {
        return NULL;
    }
    params->nlooksrange = looks;

    return Py_BuildValue("i",0);
}

PyObject *setAzimuthLooks_C(PyObject *self, PyObject *args)
{
    int looks;
    if(!PyArg_ParseTuple(args, "i", &looks))
    {
        return NULL;
    }
    params->nlooksaz = looks;

    return Py_BuildValue("i",0);
}


PyObject *setDefoMaxCycles_C(PyObject *self, PyObject *args)
{
    double defomax;
    if(!PyArg_ParseTuple(args,"d", &defomax))
    {
        return NULL;
    }
    params->defomax = defomax;

    return Py_BuildValue("i", 0);
}

PyObject *setInitMethod_C(PyObject *self, PyObject *args)
{
    int method;
    if(!PyArg_ParseTuple(args,"i", &method))
    {
        return NULL;
    }

    params->initmethod = method;

    return Py_BuildValue("i",0);
}

PyObject *setInitOnly_C(PyObject *self, PyObject *args)
{
    int method;
    if(!PyArg_ParseTuple(args,"i", &method))
    {
        return NULL;
    }

    params->initonly = method;

    return Py_BuildValue("i", 0);
}

PyObject *setMaxComponents_C(PyObject *self, PyObject *args)
{
    int num;
    if(!PyArg_ParseTuple(args,"i", &num))
    {
        return NULL;
    }
    params->maxncomps = num;

    return Py_BuildValue("i",0);
}

PyObject *setRegrowComponents_C(PyObject* self, PyObject *args)
{
    int flag;
    if(!PyArg_ParseTuple(args,"i", &flag))
    {
        return NULL;
    }
    params->regrowconncomps = flag;
    return Py_BuildValue("i", 0);
}

PyObject *setUnwrappedInput_C(PyObject* self, PyObject *args)
{
    int flag;
    if(!PyArg_ParseTuple(args,"i",&flag))
    {
        return NULL;
    }
    params->unwrapped = flag;
    return Py_BuildValue("i",0);
}

PyObject *setMinConnectedComponentFraction_C(PyObject *self, PyObject *args)
{
    double flag;
    if(!PyArg_ParseTuple(args,"d",&flag))
    {
        return NULL;
    }
    params->minconncompfrac = flag;
    return Py_BuildValue("i", 0);
}

PyObject *setConnectedComponentThreshold_C(PyObject *self, PyObject *args)
{
    double flag;
    if(!PyArg_ParseTuple(args,"d",&flag))
    {
        return NULL;
    }
    params->conncompthresh = flag;
    return Py_BuildValue("i", 0);
}

