#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

import isce
from iscesys.Component.Application import Application

NAME = Application.Parameter('name',
    public_name='name to use in greeting',
    default='World',
    type=str,
    mandatory=False,
    doc="Name you want to be called when greeted by the code."
)

LANGUAGE = Application.Parameter('language',
    public_name='language to use in greeting',
    default='English',
    type=str,
    mandatory=False,
    doc="language you want to be used when greeted by the code."
)

class Greeter(Application):

    parameter_list = (NAME, LANGUAGE)
    
    def _facilities(self):
        self.greeting = self.facility(
            'greeting',
            public_name='Greeting message',
            module = 'greetings',
            factory = 'language',
            args = (self.language,),
            mandatory=False,
            doc="""
                Generate a greeting message.
                """
        )

    def main(self):
        #The main greeting
        self.greeting(self.name)

        #some information on the internals
        from iscesys.DictUtils.DictUtils import DictUtils
        normname = DictUtils.renormalizeKey(NAME.public_name)
        print()
        print("NAME.public_name = {0}".format(NAME.public_name))
        print("normname = {0}".format(normname))
        print("self.name = {0}".format(self.name))
        if self.descriptionOfVariables[normname]['doc']:
            print("doc = {0}".format(self.descriptionOfVariables[normname]['doc']))
        if normname in self.unitsOfVariables.keys():
            print("units = {0}".format(self.unitsOfVariables[normname]['units']))
        normlang = DictUtils.renormalizeKey(LANGUAGE.public_name)
        print("LANGUAGE.public_name = {0}".format(LANGUAGE.public_name))
        print("normlang = {0}".format(normlang))
        print("self.language = {0}".format(self.language))
        if self.descriptionOfVariables[normlang]['doc']:
            print("doc = {0}".format(self.descriptionOfVariables[normlang]['doc']))
        if normlang in self.unitsOfVariables.keys():
            print("units = {0}".format(self.unitsOfVariables[normlang]['units']))

        print()
        print("For more fun, try this command line:")
        print("./greeter.py greeter.xml")
        print("./greeter.py greeterS.xml")
        print("./greeter.py greeterEC.xml")
        print("Try the different styles that are commented out in greeter.xml")
        print("Try entering data on the command line mixing with xml:")
        print("./greeter.py greeter.xml greeter.'language to use in greeting'=spanish")
        print("or try this,")
    
        cl = "./greeter.py "
        cl += "Greeter.name\ to\ use\ \ \ IN\ greeting=Juan  "
        cl += "gREETER.LANGUAGE\ TO\ USE\ IN\ GREETING=cowboy "
        cl += "greeter.name\ to\ use\ in\ greeting.units='m/s' " 
        cl += "greeter.'name to use in greeting'.doc='My new doc'"
        print("{0}".format(cl))
    
        print("etc.")

        return

    def __init__(self):
        super(Greeter, self).__init__("greeter")
        return

if __name__ == '__main__':
    greeter = Greeter()
    greeter.run()

        
