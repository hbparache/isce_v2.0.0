#!/usr/bin/env python3
import sys
import os
import json
def createHelp(env,factoryFile,installDir):
    #jng: try to have scons handle all the creation but could not figure out how
    #     so handled dir creation manually
    try:
        os.makedirs(env['HELPER_BUILD_DIR'])
    except: 
        # already exists
        pass 
    try:
        #one could probably also use __import__ but needs to make sure the
        #the cwd is prepended to the sys.path otherwise if factoryFile = __init__.py
        #it will load the first one found
        import imp
        moduleList = env['ISCEPATH']
        package = "."
        for module in moduleList:
            if installDir.count(module):
                ls = installDir.replace(module,'').split("/")
                #remove empty element
                ls = [i for i in ls if i != '']
                package = ".".join(ls)
                #when module is the same as installDir package is empty
                if not package:
                    package = [i for i in installDir.split('/') if i != ''][-1] 
        
        mod = imp.find_module(factoryFile.replace('.py',''))
        factModule = imp.load_module(factoryFile.replace('.py',''),mod[0],mod[1],mod[2])
        factoriesInfo = factModule.getFactoriesInfo()
        nameList = []
        for k,v in factoriesInfo.items():
            name = os.path.join(env['HELPER_BUILD_DIR'],k + '.hlp')
            nameList.append(name)
            v["package"] = package
            json.dump({k:v},open(name,'w'),indent=4)
    except:
        nameList = []
    return nameList,env['HELPER_DIR']
    