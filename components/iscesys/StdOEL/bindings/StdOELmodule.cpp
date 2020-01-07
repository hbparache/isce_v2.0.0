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
#include "WriterFactory.h"
#include "StdOELmodule.h"
#include <iostream>
#include <fstream>
#include <string>
#include <stdint.h>
#include <cstdio>
using namespace std;

static char * const __doc__ = "Python extension for StdOEL";

PyModuleDef moduledef = {
    // header
    PyModuleDef_HEAD_INIT,
    // name of the module
    "StdOEL",
    // module documentation string
    __doc__,
    // size of the per-interpreter state of the module;
    // -1 if this state is global
    -1,
    StdOEL_methods,
};

// initialization function for the module
// *must* be called PyInit_formslc
PyMODINIT_FUNC
PyInit_StdOEL()
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


PyObject * createWriters_C(PyObject * self, PyObject* args) 
{
	string typeOut;
	char * typeOutCh;
	string typeErr;
	char * typeErrCh;
	string typeLog;
	char * typeLogCh;
    if(!PyArg_ParseTuple(args, "|sss",&typeOutCh,&typeErrCh,&typeLogCh)) 
	{
		return NULL;  
	} 
    WriterFactory * WF = new WriterFactory();
    uint64_t ptWriter = 0;
    if(typeOut[0] == '\0')
    {
        ptWriter = (uint64_t )  WF->createWriters();
    }
    else if(typeErr[0] == '\0')
    {
        typeOut = typeOutCh;
        ptWriter = (uint64_t )  WF->createWriters(typeOut);

    }
    else if(typeLog[0] == '\0')
    {
        typeOut = typeOutCh;
        typeErr = typeErrCh;
        ptWriter = (uint64_t )  WF->createWriters(typeOut,typeErr);

    }
    else 
    {
        typeOut = typeOutCh;
        typeErr = typeErrCh;
        typeLog = typeLogCh;
        ptWriter = (uint64_t )  WF->createWriters(typeOut,typeErr,typeLog);

    }
    return Py_BuildValue("KK",ptWriter,(uint64_t) WF);
}
PyObject * finalize_C(PyObject* self, PyObject* args) 
{
	uint64_t ptStdOEL = 0;
	uint64_t ptFactory = 0;
	if(!PyArg_ParseTuple(args, "KK", &ptStdOEL,&ptFactory)) 
	{
		return NULL;  
	}
    WriterFactory * tmp = (WriterFactory *) (ptFactory);
    tmp->finalize((StdOEL *) (ptStdOEL));

	delete tmp;
	return Py_BuildValue("i", 0);
}
PyObject * init_C(PyObject* self, PyObject* args) 
{
	uint64_t ptStdOEL = 0;
	if(!PyArg_ParseTuple(args, "K", &ptStdOEL)) 
	{
		return NULL;  
	}
    StdOEL * tmp = (StdOEL *) (ptStdOEL);
    tmp->init();

	return Py_BuildValue("i", 0);
}
PyObject * setFilename_C(PyObject* self, PyObject* args) 
{
	uint64_t ptStdOEL = 0;
    char * filenameCh;
    char * whereCh;
	if(!PyArg_ParseTuple(args, "Kss", &ptStdOEL,&filenameCh,&whereCh)) 
	{
		return NULL;  
	}
    string filename = filenameCh;
    string where = whereCh;
    StdOEL * tmp = (StdOEL *) (ptStdOEL);
    tmp->setFilename(filename,where);

	return Py_BuildValue("i", 0);
}
PyObject * setFileTag_C(PyObject* self, PyObject* args) 
{
	uint64_t ptStdOEL = 0;
    char * fileTagCh;
    char * whereCh;
	if(!PyArg_ParseTuple(args, "Kss", &ptStdOEL,&fileTagCh,&whereCh)) 
	{
		return NULL;  
	}
    string fileTag = fileTagCh;
    string where = whereCh;
    StdOEL * tmp = (StdOEL *) (ptStdOEL);
    tmp->setFileTag(fileTag,where);

	return Py_BuildValue("i", 0);
}
PyObject * setTimeStampFlag_C(PyObject* self, PyObject* args) 
{
	uint64_t ptStdOEL = 0;
    int flagInt;
    char * whereCh;
	if(!PyArg_ParseTuple(args, "Kis", &ptStdOEL,&flagInt,&whereCh)) 
	{
		return NULL;  
	}
    bool flag;
    if(flagInt == 0)
    {
        flag = false;
    }
    else
    {
        flag = true;
    } 
    string where = whereCh;
    StdOEL * tmp = (StdOEL *) (ptStdOEL);
    tmp->setTimeStampFlag(flag,where);

	return Py_BuildValue("i", 0);
}
