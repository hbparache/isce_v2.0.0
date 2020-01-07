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
#include "AccessorFactory.h"
#include "DataAccessormodule.h"
#include <iostream>
#include <fstream>
#include <string>
#include <complex>
#include <stdint.h>
#include <cstdio>
using namespace std;

static char * const __doc__ = "Python extension for image API data accessors";

PyModuleDef moduledef = {
    // header
    PyModuleDef_HEAD_INIT,
    // name of the module
    "DataAccessor",
    // module documentation string
    __doc__,
    // size of the per-interpreter state of the module;
    // -1 if this state is global
    -1,
    DataAccessor_methods,
};

// initialization function for the module
// *must* be called PyInit_formslc
PyMODINIT_FUNC
PyInit_DataAccessor()
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



PyObject * createAccessor_C(PyObject* self, PyObject* args) 
{
	string filename;
	char * filenameCh;
	string filemode;
	char * filemodeCh;
	string scheme;
	char * schemeCh;
	string caster;
	char * casterCh;
	int size = 0;
	int bands = 0;
	int width = 0;
    int len = 0;
    if(!PyArg_ParseTuple(args, "ssiiis|s",&filenameCh,&filemodeCh,&size,&bands,&width,&schemeCh,&casterCh)) 
	{
		return NULL;  
	} 
	filename = filenameCh;
	filemode = filemodeCh;
	scheme = schemeCh;
    AccessorFactory * AF = new AccessorFactory();
    uint64_t ptDataAccessor = 0;
    if(casterCh[0] == '\0')
    {

        ptDataAccessor = (uint64_t )  AF->createAccessor(filename,filemode,size,bands,width,scheme);
    }
    else
    {

        caster = casterCh;
        ptDataAccessor = (uint64_t )  AF->createAccessor(filename,filemode,size,bands,width,scheme,caster);
    }
    return Py_BuildValue("KK",ptDataAccessor,(uint64_t) AF);
}
PyObject * finalizeAccessor_C(PyObject* self, PyObject* args) 
{
	uint64_t ptDataAccessor = 0;
	uint64_t ptFactory = 0;
	if(!PyArg_ParseTuple(args, "KK", &ptDataAccessor,&ptFactory)) 
	{
		return NULL;  
	}
    AccessorFactory * tmp = (AccessorFactory *) (ptFactory);
    tmp->finalize((DataAccessor *) (ptDataAccessor));

	delete tmp;
	return Py_BuildValue("i", 0);
}
PyObject * getFileLength_C(PyObject* self, PyObject* args) 
{
	uint64_t ptDataAccessor = 0;
	if(!PyArg_ParseTuple(args, "K",&ptDataAccessor)) 
	{
		return NULL;  
	}  
	int length = ((DataAccessor * )(ptDataAccessor))->getInterleavedAccessor()->getFileLength();
	return Py_BuildValue("i",length);
}
PyObject * rewind_C(PyObject* self, PyObject* args) 
{
	uint64_t ptDataAccessor = 0;
	if(!PyArg_ParseTuple(args, "K",&ptDataAccessor)) 
	{
		return NULL;  
	} 
    DataAccessor * tmp = (DataAccessor *) (ptDataAccessor);
	tmp->rewindAccessor();
	return Py_BuildValue("i",0);
}
PyObject * createFile_C(PyObject* self, PyObject* args) 
{
	uint64_t ptDataAccessor = 0;
	int length = 0;
	if(!PyArg_ParseTuple(args, "Ki",&ptDataAccessor,&length)) 
	{
		return NULL;  
	} 
    DataAccessor * tmp = (DataAccessor *) (ptDataAccessor);
	tmp->createFile(length);
	return Py_BuildValue("i",0);
}
PyObject * getTypeSize_C(PyObject* self, PyObject* args) 
{
    char * typeCh; 
    string type;
	if(!PyArg_ParseTuple(args, "s",&typeCh)) 
	{
		return NULL;  
	}  
	type = typeCh;
    int retVal = -1;
    if(type == "byte" || type == "BYTE" || type == "char" || type == "CHAR")
    {
        retVal = sizeof(char);
    }
    else if(type == "short" || type == "SHORT")
    {
        retVal = sizeof(short);
    }
    else if(type == "int" || type == "INT")
    {
        retVal = sizeof(int);
    }
    else if(type == "long" || type == "LONG")
    {
        retVal = sizeof(long);
    }
    else if(type == "float" || type == "FLOAT")
    {
        retVal = sizeof(float);
    }
    else if(type == "double" || type == "DOUBLE")
    {
        retVal = sizeof(double);
    }
    else if(type == "cbyte" || type == "CBYTE" || type == "cchar" || type == "CCHAR")
    {
        retVal = sizeof(complex<char>);
    }
    else if(type == "cshort" || type == "CSHORT")
    {
        retVal = sizeof(complex<short>);
    }
    else if(type == "cint" || type == "CINT")
    {
        retVal = sizeof(complex<int>);
    }
    else if(type == "clong" || type == "CLONG")
    {
        retVal = sizeof(complex<long>);
    }
    else if(type == "cfloat" || type == "CFLOAT")
    {
        retVal = sizeof(complex<float>);
    }
    else if(type == "cdouble" || type == "CDOUBLE")
    {
        retVal = sizeof(complex<double>);
    }
    else
    {
        cout << "Error. Unrecognized data type " << type <<  endl;
        
        ERR_MESSAGE;
    }
	return Py_BuildValue("i",retVal);
}
