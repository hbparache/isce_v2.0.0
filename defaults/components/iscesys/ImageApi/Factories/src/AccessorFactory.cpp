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



#include "AccessorFactory.h"
#include "CasterFactory.h"
#include "InterleavedFactory.h"
#include "DataCaster.h"
#include "InterleavedAccessor.h"
#include "DataAccessor.h"
#include "DataAccessorCaster.h"
#include "DataAccessorNoCaster.h"
using namespace std;

DataAccessor * AccessorFactory::createAccessor(string filename,string accessMode, int size, int bands,int width, string interleaved,string caster)
{
    
        CasterFactory CF;
        InterleavedFactory IF;
        InterleavedAccessor * interleavedAcc =  IF.createInterleaved(interleaved); 
        interleavedAcc->init(filename,accessMode,size,bands,width);        
        DataCaster * casterD = CF.createCaster(caster);               
        return  new  DataAccessorCaster(interleavedAcc, casterD);
}
DataAccessor * AccessorFactory::createAccessor(string filename,string accessMode, int size, int bands,int width, string interleaved)
{

        InterleavedFactory IF;
        InterleavedAccessor * interleavedAcc = IF.createInterleaved(interleaved); 
        interleavedAcc->init(filename,accessMode,size,bands,width);        
        return new  DataAccessorNoCaster(interleavedAcc);
}
void AccessorFactory::finalize(DataAccessor * dataAccessor)
{
    dataAccessor->finalize();
}
