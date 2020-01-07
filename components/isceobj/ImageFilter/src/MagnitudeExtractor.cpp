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



#include <iostream>
#include <limits>
#include <cmath>
#include "MagnitudeExtractor.h"

using namespace std;

void MagnitudeExtractor::extract()
{
    int eof = 1;
    //loop through the image. The DataType size is ImageIn->DataSizeIn.  
    int width = ImageIn->getWidth();  
    int bands = ImageIn->getBands();  
    int sizeIn = ImageIn->getSizeIn();  
    char * bufIn = new char[width*sizeIn*bands];
    char * bufOut = new char[width*(sizeIn/2)*bands];
    int cnt = StartLine;
    ImageIn->initSequentialAccessor(StartLine);
    while(true)
    {
        eof = ImageIn->getLineSequential(bufIn);
        ++cnt;
        if(eof < 0 || cnt > EndLine)
        {
            break;
        }
        for(int i = 0; i < width*bands; ++i)
        {
            //we don't know a priori the data type so at this point try to figure the right casting
            if(sizeIn/2 == sizeof(float))
            {
                float * x = (float *) &bufIn[i*sizeIn];
                float * y = (float *) &bufIn[i*sizeIn + sizeIn/2];
                float magnitude = sqrt((*x)*(*x) + (*y)*(*y));
                (* (float *) &bufOut[i*sizeIn/2]) = magnitude;
            }   
            else if(sizeIn/2 == sizeof(double))
            {
                double * x = (double *) &bufIn[i*sizeIn];
                double * y = (double *) &bufIn[i*sizeIn + sizeIn/2];
                double magnitude = sqrt((*x)*(*x) + (*y)*(*y));
                (* (double *) &bufOut[i*sizeIn/2]) = magnitude;
            }
            else
            {
                cout << "Datatype size not supported." << endl;
                ERR_MESSAGE;
            }
        }
        ImageOut->setLineSequential(bufOut);
    }
    delete [] bufIn;
    delete [] bufOut;
}

