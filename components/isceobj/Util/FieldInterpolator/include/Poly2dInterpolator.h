#ifndef Poly2dInterpolator_h
#define Poly2dInterpolator_h


#ifndef MESSAGE
#define MESSAGE cout << "file " << __FILE__ << " line " << __LINE__ << endl;
#endif
#ifndef ERR_MESSAGE
#define ERR_MESSAGE cout << "Error in file " << __FILE__ << " at line " << __LINE__  << " Exiting" <<  endl; exit(1);
#endif

#include <cmath>
#include "FieldInterpolator.h"
#include "poly2d.h"

class Poly2dInterpolator: public FieldInterpolator
{
    public:
        Poly2dInterpolator():FieldInterpolator(){}
        virtual ~Poly2dInterpolator(){delete [] Data;}

        double getField(double row, double col);

    protected:
        cPoly1d poly; 
};

#endif Poly2dInterpolator_h
