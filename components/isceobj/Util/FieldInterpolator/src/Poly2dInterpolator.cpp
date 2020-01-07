#include <cmath>
#include "Poly2dInterpolator.h"

void Poly2dInterpolator::getField(double row, double col)
{
    double res;

    res = evalPoly2d(&poly,row,col);
    return res;
}
