#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2009 to the present, California Institute of Technology.
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
# Authors: Eric Gurrola, Giangi Sacco
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



from __future__ import print_function
import sys
import operator

from iscesys.Component.Component import Component
from iscesys.DictUtils.DictUtils import DictUtils as DU

class CmdLinePropDict(object):
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = dict()
        return cls._instance

class CmdLineFactDict(object):
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = dict()
        return cls._instance

class CmdLineMiscDict(object):
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = dict()
        return cls._instance

class CmdLineDocDict(object):
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = dict()
        return cls._instance

class CmdLineUnitsDict(object):
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = dict()
        return cls._instance

## A decorator that makes a function taking self as the 1st argument
def curried(func):
    def curried_func(self, *args):
        return func(self, *args)
    return curried_func


class StepHelper(object):
    """This Mixin help sub class's _parameter_steps() methods
    call functions.
    """
    @staticmethod
    def compose(f, g, fargs=(), gargs=(), fkwargs={}, gkwargs={}):
        """compose(f, g)() --> f(g())"""
        from functools import partial
        def fog(*args, **kwargs):
            return  (
                partial(f, *fargs, **fkwargs)(
                    partial(g, *gargs, **gkwargs)(
                        *args, **kwargs
                         )
                    )
                )
        return fog

    def attrgetter(self, attr, attribute=None):
        inst = getattr(self, attribute) if attribute else self
        return getattr(inst, attr)

    def attrsetter(self, attr, value, attribute=None):
        inst = getattr(self, attribute) if attribute else self
        return setattr(inst, attr, value)

    def delayed_attrgetter(self, attr, attribute=None):
        return lambda : self.attrgetter(attr, attribute=attribute)

    def delayed_attrsetter(self, attr, attribute=None):
        return lambda value: self.attrsetter(self,
                                             attr,
                                             value,
                                 attribute=attribute)

    ## self.delayed_attrsetter(attr, delayed_attr
    def delayed_attrcopy_from_to(self, attri, attrf, attribute=None):
        return lambda : self.attrsetter(
            attrf,
            self.attrgetter(
                attri,
                attribute=attribute
                ),
            attribute=attribute
            )

    pass


## Application base class
class Application(Component, StepHelper):
    cont_string = ''

    def run(self, *cmdLine):
        #since we execute the run method and not the main
        #return the exist status of the main just in case somebody needs it
        exitStatus = 0

        ## Check not any occurance of a steps related command keyword
        if any([operator.contains(
                [y[0] for y in [x.split('=') for x in self.cmdline]], item) for
                item in ("--steps", "--dostep", "--start", "--end")]
              ):
            print("Processing steps")
            self._steps()
            self._processSteps()
        else:
            exitStatus = self.main()

        #Run the user's finalize method
        self._finalize()
        return exitStatus








    # Method allows uses to pass cmdline externally as well
    def _processCommandLine(self,cmdline=None):
        from iscesys.Parsers.Parser import Parser

        if cmdline:
            if(isinstance(cmdline,str)):
                #just in case a string is passed, turn it into a list
                cmdline = [cmdline]
            self.cmdline = cmdline
        else:
            self.cmdline = self._getCommandLine()


        #process the command line and return a dictionary of dictionaries with
        # components per each node.
        # propDict contains the property for each component.
        # factDict contains the info for the component factory.
        # miscDict might contain doc and units. opts are the command lines
        # preceeded by --
        PA = Parser()
        propDict, factDict, miscDict, self._argopts = PA.commandLineParser(
            self.cmdline
            )

        CmdLinePropDict().update(propDict)
        CmdLineFactDict().update(factDict)
        CmdLineMiscDict().update(miscDict)

        #extract doc from miscDict
        docDict = DU.extractDict(miscDict, 'doc')
        CmdLineDocDict().update(docDict)

        #extract units from miscDict
        unitsDict = DU.extractDict(miscDict, 'units')
        CmdLineUnitsDict().update(unitsDict)

        # self.catalog stores the properties for all configurable components
        # as a dictionary of dictionaries which wil be used to recursively
        # initialize the components
        if propDict:
            # propDict contains a only the Application dictionary at the top
            # level
            self.catalog = propDict[list(propDict.keys())[0]]

        self._cmdLineDict = (factDict, docDict, unitsDict)
        return None

    def _getCommandLine(self):
#        if len(sys.argv) < 2:
#            print("An input file is required.")
#            self.Usage()
#            sys.exit(0)
        argv = sys.argv[1:]
        return argv
    def Usage(self):
        """Method that the developer may replace in order to message to the user
            to instruct how to run teh application
        """
    def help_steps():
        """
        Method to print a helpful message when using steps
        """

    def step(self, name, attr=None, local=None, func=None, args=(), delayed_args=(), kwargs={},
             doc="Please provide a helpful message in the step declaration"):

        if isinstance(name, str):
            self.step_list.append(name)
        else:
            raise TypeError("First argument to step must be a string giving a unique name to the step")

        if args and delayed_args:
            raise ValueError("Can only evaluate args or delayed args")


        self.step_num = len(self.step_list) - 1
        self._dictionaryOfSteps[name] = {'step_index' : self.step_num,
                                         'local' : local,
                                         'attr' : attr,
                                         'func' : func,
                                         'args' : args,
                                         'delayed_args' : delayed_args,
                                         'kwargs' : kwargs,
                                         'doc' : doc}
        return None

    ## Dump Application._pickObj and renderProcDoc().
    def dumpPickleObj(self, name):
        import pickle
        import os
        if not os.path.isdir(self.pickleDumpDir):
            os.mkdir(self.pickleDumpDir)

        with open(os.path.join(self.pickleDumpDir, name), 'wb') as PCKL:
            print("Dumping the application's pickle object %s to file  %s" %
                  (self._pickleObj, os.path.join(self.pickleLoadDir, name)))
            pickle.dump(getattr(self, self._pickleObj), PCKL, protocol=pickle.HIGHEST_PROTOCOL)

        self.renderProcDoc()
        return None


    ## Load Application._pickleObj from Appication.pickleLoadDir
    def loadPickleObj(self, name):
        import  pickle
        import os
        try:
            with open(os.path.join(self.pickleLoadDir, name), 'rb') as PCKL:
                setattr(self, self._pickleObj, pickle.load(PCKL))
                print(
                    "Loaded the application's pickle object, %s from file %s" %
                    (self._pickleObj, os.path.join(self.pickleLoadDir, name))
                    )
        except IOError:
            print("Cannot open %s", os.path.join(self.pickleLoadDir, name))
        return None


    def _processSteps(self):
        import getopt
        start = 0
        startName = self.step_list[0]
        end = self.step_num
        endName = self.step_list[self.step_num-1]


        opts, args = getopt.getopt(self._argopts, 's:e:d:',
                                   ['start=', 'end=', 'dostep=', 'steps'])
        for o, a in opts:
            if o in ('--start', '-s'):
                startName = a
            elif o in ('--end', '-e'):
                endName = a
            elif o in ('--dostep', '-d'):
                startName = a
                endName = a
            elif o == "--steps":
                pass
            else:
                print("unhandled option, arg ", o, a)

        print("self.step_list = ", self.step_list)
        if startName in self.step_list:
            start = self.step_list.index(startName)
        else:
            print("ERROR: start=%s is not one of the named steps" % startName)
            sys.exit(0)

        if endName in self.step_list:
            end = self.step_list.index(endName)
        else:
            print("ERROR: end=%s is not one of the named steps" % endName)
            sys.exit(0)

        if start > end:
            print(
                "ERROR: start=%s, step number %d comes after end=%s, step number %d"
                %
                (startName, start, endName, end)
                )
            sys.exit(0)

        if start > 0:
            name = self.step_list[start-1]
            print("start, name = ", start, name)
            self.loadPickleObj(name)

#        print("self._dictionaryOfSteps['filter'] = ",
#              self._dictionaryOfSteps['filter'])

        for s in self.step_list[start:end+1]:
            func = self._dictionaryOfSteps[s]['func']
            args = self._dictionaryOfSteps[s]['args']
            delayed_args = self._dictionaryOfSteps[s]['delayed_args']
            kwargs = self._dictionaryOfSteps[s]['kwargs']
            locvar = self._dictionaryOfSteps[s]['local']
            attr = self._dictionaryOfSteps[s]['attr']

            pargs = ()
            if args:
                for arg in args:
                    pargs += (arg,)
                    pass
                pass
            else:
                for arg in delayed_args:
                    print("eval:",arg)
                    pargs += (eval(arg),)
                    pass
                pass

            result = func(*pargs, **kwargs)
            if locvar:
                locals()[locvar] = result
                pass
            if attr:
                setattr(self, attr, result)
                pass

            self.dumpPickleObj(s)

            if self.step_list.index(s) < len(self.step_list)-1:
                print("The remaining steps are (in order): ",
                      self.step_list[self.step_list.index(s)+1:])
            else:
                print("The is the final step")

            pass # steps loops ends here
        return None


    def __init__(self, family='', name='',cmdline=None):
        self.name = name
        self._dictionaryOfSteps = {}
        self._argopts = []
        self.step_list = []
        self._processCommandLine(cmdline)
        super(Application, self).__init__(family=family, name=name)
        return
