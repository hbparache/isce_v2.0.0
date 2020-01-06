#!/usr/bin/env python3

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2013 to the present, California Institute of Technology.
# ALL RIGHTS RESERVED. United States Government Sponsorship acknowledged.
# Any commercial use must be negotiated with the Office of Technology Transfer
# at the California Institute of Technology.
# 
# This software may be subject to U.S. export control laws. By accepting this
# software, the user agrees to comply with all applicable U.S. export laws and
# regulations. User has the responsibility to obtain export licenses,  or other
# export authority as may be required before exporting such information to
# foreign countries or providing access to foreign persons.
# 
# Installation and use of this software is restricted by a license agreement
# between the licensee and the California Institute of Technology. It is the
# User's responsibility to abide by the terms of the license agreement.
#
# Author: Eric Gurrola
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




"""
greeter:
An ISCE application to greet the user illustrating the usage of
Application.Parameter to expose configurable parameters to the user
through an input xml file.  

The accompanying greeter.xml file illustrates various formats 
allowed for the input file as well of examples that will not work.

To run this example type,

> ./greeter.py greeter.xml

or, one of the following:

> ./greeter.py --greeter.name\ to\ use\ in\ greeting=Joe
> ./greeter.py --greeter."name to use in greeting"=Joe
"""

from __future__ import print_function

import isce
from iscesys.Component.Application import Application

NAME = Application.Parameter('name',
    public_name='name to use in greeting',
    default="World",
    type=str,
    mandatory=True,
    doc="Name you want to be called when greeted by the code."
)

class Greeter(Application):
    """
    """
    parameter_list = (NAME,)
    #facility_list = ()

    def main(self):
        print("Hello, {0}!".format(self.name))

        print()
        print("Some information")
        from iscesys.DictUtils.DictUtils import DictUtils
        normname = DictUtils.renormalizeKey(NAME.public_name)
        print("NAME.public_name = {0}".format(NAME.public_name))
        print("normname = {0}".format(normname))
        print("self.name = {0}".format(self.name))
        if self.descriptionOfVariables[normname]['doc']:
            print("doc = {0}".format(self.descriptionOfVariables[normname]['doc']))
        if normname in self.unitsOfVariables.keys():
            print("units = {0}".format(self.unitsOfVariables[normname]['units']))

        print()
        print("For more fun, try this command line:")
        print("./greeter.py greeter.xml")
        print("Try the different styles that are commented out in greeter.xml")
        print("Try entering data on the command line:")
        print("./greeter.py greeter.'name to use in greeting'=Jane")
        print("or try this,")
    
        cl = "./greeter.py "
        cl += "Greeter.name\ to\ use\ \ \ IN\ greeting=Juan "
        cl += "greeter.'name to use in greeting'.units='m/s' " 
        cl += "greeter.'name to use in greeting'.doc='My new doc string'"
    
        print("{0}".format(cl))
    
        print("etc.")

        return

    def __init__(self):
        super(Greeter, self).__init__("greeter")
        return

if __name__ == '__main__':
    greeter = Greeter()
    greeter.run()


        
