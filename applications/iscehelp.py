#!/usr/bin/env python3
#Author:Giangi Sacco
#Copyright 2009-2014, by the California Institute of Technology.
import isce
import os
import sys
import json
import argparse
import collections
import importlib
class Helper(object):

    def getRegistered(self):
        #Register all the factory that want to provide help
        #Each .hlp file has a json structure  like
        '''
        {TypeName
                     {'args':
                           {
                            #positional arguments have has key the position in str format
                            #since json only allows keys to be string
                            '0':{value':values,'type':type},
                            '1':{'value':values,'type':type}
                            #keyword arguments have the name of the argument as key
                            argname:{'value':values,'type':type}
                            },
                     'factory':factory,
                     'package':package,
                     }
              }
        '''
        registered = {}
        helplist = os.listdir(self._helpDir)
        for name in helplist:
            fullname = os.path.join(self._helpDir,name)
            if not name.endswith('.hlp'):
                continue
            with open(fullname) as fp:
                registered.update(json.load(fp))

        return collections.OrderedDict(sorted(registered.items()))

    def getTypeFromFactory(self,factory):
        instanceType = 'N/A'
        for k,v in self._registered.items():
            if v['factory'] == factory:
                instanceType = k
                break
        return instanceType

    def getInstance(self,typeobj):
        obj2help = self._registered[typeobj]
        args,kwargs = self.getPosAndKwArgs(obj2help)
        factory = getattr(importlib.import_module(obj2help['package']),obj2help['factory'])
        return factory(*args,**kwargs)

    def convert(self,value,type_):

        try:
            module = importlib.import_module('builtins')
            ret = getattr(module,type_)(value)
        except:
            print("Cannot convert",value,"to a type",type_)
            raise Exception
        return ret

    def askHelp(self, instance, steps=False):
        #since it can be called externally, make sure that we remove the
        #arguments that are not understood by the isce Parser
        sys.argv = [sys.argv[0]]
        instance._parameters()
        instance.initProperties({})
        instance._init()
        instance._facilities()
        self.helper(instance, steps)
    def getPosAndKwArgs(self,obj):
        args = []
        kwargs = {}
        if self._inputs.args:#otherwise no args present
            for arg,i in zip(self._inputs.args,range(len(self._inputs.args))):
                try:
                    #positional argument
                    args.append(self.convert(arg,obj['args'][str(i)]['type']))
                except Exception as e:
                    try:
                        kw,val = arg.split("=")
                        kwargs[kw] = self.convert(val,obj['args'][kw]['type'])
                    except Exception as e:
                        print(e)
                        raise

        return (args,kwargs)

    def step_help(self, instance):
            instance.help_steps()
            instance._add_methods()
            instance._steps()
            print()
            print("Command line options for steps processing are formed by")
            print("combining the following three options as required:\n")
            print("'--start=<step>', '--end=<step>', '--dostep=<step>'\n")
            print("The step names are chosen from the following list:")
            print()
            npl = 5
            nfl = int(len(instance.step_list)/npl)
            for i in range(nfl):
                print(instance.step_list[i*npl:(i+1)*npl])
            if len(instance.step_list) % npl:
                print(instance.step_list[nfl*npl:])
            print()
            print("If --start is missing, then processing starts at the "+
                "first step.")
            print("If --end is missing, then processing ends at the final "+
                "step.")
            print("If --dostep is used, then only the named step is "+
                "processed.")
            print()
            print("In order to use either --start or --dostep, it is "+
                "necessary that a")
            print("previous run was done using one of the steps options "+
                "to process at least")
            print("through the step immediately preceding the starting "+
                "step of the current run.")
            print()
            sys.exit(0)


    def helper(self,instance,steps=False):
        #if facility is None we print the top level so the recursion ends right away
        #if facility is defined (not None) and is not part of teh facilities
        # then keep going down the tree structure

        instance.help()
        print()
        try:
            instance.Usage()
            print()
            if steps:
                self.step_help(instance)
                sys.exit(0)
        except SystemExit as x:
            sys.exit(0)
        finally:
            pass

        #sometime there is no help available. Postpone the printing until
        #there is something to print for sure
        fullMessage = ""
        fullMessage = "\nSee the table of configurable paramters listed in the table\n"
        fullMessage += "below for a list of parameters that may be specified in the\n"
        fullMessage += "input file.  See example input xml files in the isce 'examples'\n"
        fullMessage += "directory.  Read about the input file in the ISCE.pdf document.\n"

#        maxname = max(len(n) for n in self.dictionaryOfVariables.keys())
#        maxtype = max(len(str(x[1])) for x in self.dictionaryOfVariables.values())
#        maxman = max(len(str(x[2])) for x in self.dictionaryOfVariables.values())
#        maxdoc = max(len(x) for x in self.descriptionOfVariables.values())
        maxname = 27
        maxtype = 10
        maxman = 10
        maxdoc = 30
        underman = "="*maxman
        undertype = "="*maxtype
        undername = "="*maxname
        underdoc = "="*maxdoc
        spc = " "
        n = 1
        spc0 = spc*n

        fullMessage += "\nThe user configurable inputs are given in the following table.\n"
        fullMessage += "Those inputs that are of type 'component' are also listed in\n"
        fullMessage += "table of facilities below with additional information.\n"
        fullMessage += "To configure the parameters, enter the desired value in the\n"
        fullMessage += "input file using a property tag with name = to the name\n"
        fullMessage += "given in the table.\n"

        line  = "name".ljust(maxname,' ')+spc0+"type".ljust(maxtype,' ')
        line += spc0+"mandatory".ljust(maxman,' ')+spc0+"doc".ljust(maxdoc,' ')

        fullMessage += line + '\n'

        line = undername+spc0+undertype+spc0+underman+spc0+underdoc

        fullMessage += line + '\n'

        #make sure that there is something to print
        shallPrint = False
        for x, y in instance.dictionaryOfVariables.items():
            skip = False
            try:
                z = instance.descriptionOfVariables[x]['doc']
            except:
                try:
                    z = instance._dictionaryOfFacilities[x]['doc']
                except:
                    skip = True
            if not skip:
                shallPrint = True
                try:
                    yt = str(y[1]).split("'")[1]
                except:
                    yt = str(y[1])

                lines = []
                self.cont_string = ''
                lines.append(self.columnate_words(x, maxname, self.cont_string))
                lines.append(self.columnate_words(yt, maxtype, self.cont_string))
                lines.append(self.columnate_words(y[2], maxman, self.cont_string))
                lines.append(self.columnate_words(z, maxdoc, self.cont_string))
                nlines = max(map(len,lines))
                for row in lines:
                    row += [' ']*(nlines-len(row))
                for ll in range(nlines):
                    fullMessage  += lines[0][ll].ljust(maxname,' ')
                    fullMessage += spc0+lines[1][ll].ljust(maxtype,' ')
                    fullMessage += spc0+lines[2][ll].ljust(maxman,' ')
                    fullMessage += spc0+lines[3][ll].ljust(maxdoc,' ') + '\n'
#            line  = spc0+x.ljust(maxname)+spc0+yt.ljust(maxtype)
#            line += spc0+y[2].ljust(maxman)+spc0+z.ljust(maxdoc)
#            print(line)
        if(shallPrint):
            print(fullMessage)
        else:
            print("No help available\n")
        #only print the following if there are facilities
        if(instance._dictionaryOfFacilities.keys()):
            #maxname = max(len(n) for n in self._dictionaryOfFacilities.keys())
            maxname = 15
            undername = "="*maxname

    #        maxmod = max(
    #            len(x['factorymodule']) for x in
    #            self._dictionaryOfFacilities.values()
    #            )
            maxmod = 17
            undermod = "="*maxmod

    #        maxfac = max(
    #            len(x['factoryname']) for x in
    #            self._dictionaryOfFacilities.values()
    #            )
            maxfac = 17
            underfac = "="*maxfac

    #        maxarg = max(
    #            len(str(x['args'])) for x in self._dictionaryOfFacilities.values()
    #            )
            maxarg = 20
            underarg = "="*maxarg

    #        maxkwa = max(
    #            len(str(x['kwargs'])) for x in
    #            self._dictionaryOfFacilities.values()
    #            )
            maxkwa = 7
    #        underkwa = "="*max(maxkwa, 6)
            underkwa = "="*maxkwa
            spc = " "
            n = 1
            spc0 = spc*n
            print()
            print("The configurable facilities are given in the following table.")
            print("Enter the component parameter values for any of these "+
                "facilities in the")
            print("input file using a component tag with name = to "+
                "the name given in")
            print("the table. The configurable parameters for a facility "+
                "are entered with ")
            print("property tags inside the component tag. Examples of the "+
                "configurable")
            print("parameters are available in the examples/inputs directory.")
            print("For more help on a given facility run")
            print("iscehelp.py -t type")
            print("where type (if available) is the second entry in the table")
            print()

            line  = "name".ljust(maxname)+spc0+"type".ljust(maxmod)

            print(line)
            line  = " ".ljust(maxname)+spc0+" ".ljust(maxmod)

            print(line)
            line = undername+spc0+undermod
            print(line)

            for x, y in instance._dictionaryOfFacilities.items():

                lines = []
                self.cont_string = ''
                lines.append(self.columnate_words(x, maxname, self.cont_string))
                z = self.columnate_words(self.getTypeFromFactory(y['factoryname']),maxmod, self.cont_string)
                lines.append(z)

                nlines = max(map(len,lines))
                for row in lines:
                    row += [' ']*(nlines-len(row))
                for ll in range(nlines):
                    out  = lines[0][ll].ljust(maxname)
                    out += spc0+lines[1][ll].ljust(maxmod)
                    print(out)
            '''
            line  = "name".ljust(maxname)+spc0+"package".ljust(maxmod)
            line += spc0+"factory".ljust(maxfac)+spc0+"args".ljust(maxarg)
            line += spc0+"kwargs".ljust(maxkwa)
            print(line)
            line  = " ".ljust(maxname)+spc0+" ".ljust(maxmod)
            line += spc0+" ".ljust(maxfac)+spc0+"default".ljust(maxarg)
            line += spc0+"default".ljust(maxkwa)
            print(line)
            line = undername+spc0+undermod+spc0+underfac+spc0+underarg+spc0+underkwa
            print(line)

            for x, y in instance._dictionaryOfFacilities.items():

                lines = []
                self.cont_string = ''
                lines.append(self.columnate_words(x, maxname, self.cont_string))
                z = self.columnate_words(y['factorymodule'],maxmod, self.cont_string)
                lines.append(z)
                z = self.columnate_words(y['factoryname'],maxfac, self.cont_string)
                lines.append(z)
                z = self.columnate_words(str(y['args']), maxarg, self.cont_string)
                lines.append(z)
                z = self.columnate_words(str(y['kwargs']), maxkwa,self.cont_string)
                lines.append(z)

                nlines = max(map(len,lines))
                for row in lines:
                    row += [' ']*(nlines-len(row))
                for ll in range(nlines):
                    out  = lines[0][ll].ljust(maxname)
                    out += spc0+lines[1][ll].ljust(maxmod)
                    out += spc0+lines[2][ll].ljust(maxfac)
                    out += spc0+lines[3][ll].ljust(maxarg)
                    out += spc0+lines[4][ll].ljust(maxkwa)
                    print(out)
            '''
#            line  = spc0+x.ljust(maxname)+spc0+y['factorymodule'].ljust(maxmod)
#            line += spc0+y['factoryname'].ljust(maxfac)
#            line += spc0+str(y['args']).ljust(maxarg)
#            line += spc0+str(y['kwargs']).ljust(maxkwa)
#            print(line)

        return sys.exit(1)
    def columnate_words(self, s, n, cont=''):
        """
        arguments = s (str), n (int), [cont (str)]
        s is a sentence
        n is the column width
        Returns an array of strings of width <= n.
        If any word is longer than n, then the word is split with
        continuation character cont at the end of each column
        """
        #Split the string s into a list of words
        a = s.split()

        #Check the first word as to whether it fits in n columns
        if len(a[0]) > n:
            y = [x for x in self.nsplit(a[0]+" ", n, cont)]
        else:
            y = [a[0]]
        cnt = len(y[-1])

        for i in range(1, len(a)):
            cnt += len(a[i])+1
            if cnt <= n:
                y[-1] += " "+a[i]
            else:
                y += self.nsplit(a[i], n, cont)
                cnt = len(y[-1])
        return y

    def nsplit(self, s, nc, cont=''):
        x = []
        ns = len(s)
        n = nc - len(cont)
        for i in range(int(ns/n)):
            x.append(s[i*n:(i+1)*n]+cont)
        if ns%n:
            x.append(s[int(ns/n)*n:])
        return x


    def printInfo(self,type_,helpIfNoArg = False, steps=False):
        try:
            sortedArgs = collections.OrderedDict(sorted(self._registered[type_]['args'].items()))
            print("\nType:",type_)
            for arg,val in sortedArgs.items():
                if(arg.isdigit()):
                    print("Positional argument ",arg,", type ", val['type'],sep="")
                else:
                    print("Keyword argument ",arg,", type ", val['type'],sep="")

                if isinstance(val['value'],list):
                    print("Possible values for ",arg,": ", sep='',end="")
                    for pv in val['value']:
                        print(pv,"",end="")
                    print('\n')
        except:
            if helpIfNoArg:
                 instance = self.getInstance(type_)
                 self.askHelp(instance, self._inputs.steps)
            else:
                print("\nType:",type_, "no arguments required")




    def printAll(self):
        for k in self._registered.keys():
            self.printInfo(k)


    def run(self):
        self.parse()
        sys.argv = [sys.argv[0]]

        noArgs = True
        for k,v in self._inputs._get_kwargs():
            if(v):
                noArgs = False
                break

        if self._inputs.info or noArgs:
            #if no arguments provided i.e. self._input has all the attribute = None
            #then print the list of all available helps
            self.printAll()
        elif self._inputs.type and not self._inputs.args:
            #if only -t type is provided print how to get help for that specific type
            self.printInfo(self._inputs.type,helpIfNoArg=True)
        elif self._inputs.type and (self._inputs.args):
            #if type and arguments are provided then provide help for that type
            if self._inputs.type in self._registered:
                instance = self.getInstance(self._inputs.type)
                self.askHelp(instance, self._inputs.steps)
            else:
                print("Help for",self._inputs.type,"is not available. Run iscehelp.py"+\
                      " with no options to see the list of available type of objects" +\
                      " one can get help for")
                sys.exit(1)
        elif self._inputs.type and self._inputs.steps and not self._inputs.args:
            #if only -t type is provided print how to get help for that specific type
            self.printInfo(self._inputs.type, helpIfNoArg=True,
                steps=self._inputs.steps)
        elif self._inputs.type and (self._inputs.args) and self._inputs.steps:
            #if type and arguments are provided then provide help for that type
            if self._inputs.type in self._registered:
                instance = self.getInstance(self._inputs.type)
                self.askHelp(instance, self._inputs.steps)
            else:
                print("Help for",self._inputs.type,"is not available. Run iscehelp.py"+\
                      " with -i (--info)  to see the list of available type of objects" +\
                      " one can get help for")
                sys.exit(1)



    def parse(self):
        epilog = 'Run iscehelp.py with no arguments or with -i option to list the available object\n'
        epilog += 'types for which help is provided\n'
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,epilog=epilog)
        parser.add_argument('-i','--info',dest='info',action='store_true',help='Provides the list of registered object types')
        parser.add_argument('-t','--type',dest='type',type=str,help='Specifies the object type for which help is sought')
        parser.add_argument('-a','--args',dest='args',type=str,nargs='+',help='Set of positional and keyword arguments '\
                                                                        +'that the factory of the object "type" takes.'\
                                                                        + 'The keyword arguments are specified as keyword=value with no spaces.')
        parser.add_argument('-s','--steps',dest='steps',action='store_true',help='Provides the list of steps in the help message')

        self._inputs = parser.parse_args()
    def __init__(self):
        import isce
        #the directory is defined in SConstruct
        self._helpDir = os.path.join(isce.__path__[0],'helper')
        self._registered = self.getRegistered()
        self._inputs = None

def main():
    hp = Helper()
    hp.run()
if __name__ == '__main__':
    main()
