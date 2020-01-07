#include "InterleavedFactory.h"
#include "InterleavedAccessor.h"
#include "BIPAccessor.h"
#include "BILAccessor.h"
#include "BSQAccessor.h"
using namespace std;

InterleavedAccessor * InterleavedFactory::createInterleaved(string sel)
{
    if(sel == "BIL")
    {
            return  new  BILAccessor();
    }
    else if(sel == "BIP")
    {
            return  new  BIPAccessor();
    }
    else if(sel == "BSQ")
    {
            return  new  BSQAccessor();
    }
    else
    {
        cout << "Error. " << sel << " is an unrecognized Interleaved Scheme."<< endl;
        ERR_MESSAGE;
    }
}
