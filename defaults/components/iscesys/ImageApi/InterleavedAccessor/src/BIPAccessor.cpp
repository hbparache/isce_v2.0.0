#include <iostream>
#include <fstream>
#include "BIPAccessor.h"

using namespace std;
void BIPAccessor::setData(char * buf, int row, int col, int numEl)
{
    streampos posNow = ((streampos) row*LineWidth*Bands*SizeV) + ((streampos) col*Bands*SizeV);
    FileObject.seekp(posNow);
    FileObject.write(buf,numEl*Bands*SizeV);
    //the good flag gets set but not the eof for some reason, so assume eof when good is set false
    if(!FileObject.good())
    {
        NoGoodFlag = 1;
        EofFlag = -1;
    }
}
void BIPAccessor::setDataBand(char* buf, int row, int col, int numEl, int band)
{
    streampos posNow = ((streampos) row*LineWidth*Bands*SizeV) + ((streampos) col*Bands*SizeV) + (streampos)band*SizeV;

    if(Bands > 1)
    {
        for(int i=0; i<numEl; i++)
        {
            FileObject.seekp(posNow);
            FileObject.write(&buf[i*SizeV], SizeV);
            posNow += Bands*SizeV;
        }
    }
    else
    {
        setData(buf, row, col, numEl);
    }
}
    
void BIPAccessor::getData(char * buf, int row, int col, int & numEl)
{
    streampos posNow = ((streampos)row*LineWidth*Bands*SizeV) + ((streampos)col*Bands*SizeV);
    FileObject.seekg(posNow);
    FileObject.read(buf,numEl*Bands*SizeV);
    numEl = FileObject.gcount()/(SizeV*Bands);
    
    
    //the good flag gets set but not the eof for some reason, so assume eof when good is set false
    if(!FileObject.good())
    {
        NoGoodFlag = 1;
        EofFlag = -1;
    }
}
void BIPAccessor::getDataBand(char * buf, int row, int col, int &numEl, int band)
{
    int actualRead = 0;
    streampos posNow = ((streampos) row*LineWidth*Bands*SizeV) + ((streampos)col*Bands*SizeV) + (streampos)band*SizeV;

    if(Bands > 1)
    {
        for(int i=0;i<numEl;i++)
        {
            FileObject.seekg(posNow);
            FileObject.read(&buf[i*SizeV], SizeV);
            actualRead += FileObject.gcount()/(SizeV);
            posNow += Bands*SizeV;
        }
        numEl = actualRead; 

        if (!FileObject.good())
        {
            NoGoodFlag = 1;
            EofFlag = -1;
        }
    }
    else
    {
//        std::cout << "Line = " << row << " Offset = " << posNow << std::endl;
        actualRead = numEl;
        getData(buf, row, col, actualRead);
        numEl = actualRead;
    }
}
