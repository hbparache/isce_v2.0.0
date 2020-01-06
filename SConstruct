#!/usr/bin/env python

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2010 to the present, California Institute of Technology.
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
# Author: Giangi Sacco
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



import os
import sys

if ((sys.version_info[0] > 2)):
    print ("Sorry. Compiling requires a python version < 3")
    raise Exception

if 'SCONS_CONFIG_DIR' in os.environ:
    sconsConfigDir = os.environ['SCONS_CONFIG_DIR']
else:
    print("Error. Need to set the variable SCONS_CONFIG_DIR in the shell environment")
    raise Exception

from configuration import sconsConfigFile
#allow scons to take the input argument --setupfile=someOtherFile to allow change of the default SConfigISCE
AddOption('--setupfile',dest='setupfile',type='string',default='SConfigISCE')

env = Environment(ENV = os.environ)
sconsSetupFile = GetOption('setupfile')

sconsConfigFile.setupScons(env,sconsSetupFile)
#add some information that are necessary to build the framework such as specific includes, libpath and so on
buildDir = env['PRJ_SCONS_BUILD']
libPath = os.path.join(buildDir,'libs')
#this is the directory where all the built library are put so they can easily be found during linking
env['PRJ_LIB_DIR'] = libPath

# add the libPath to the LIBPATH environment that is where all the libs are serched
env.AppendUnique(LIBPATH = [libPath])

# add the modPath to the FORTRANMODDIR environment that is where all the fortran mods are searched

#not working yet
modPath = os.path.join(buildDir,'mods')
env['FORTRANMODDIR'] =  modPath
env.AppendUnique(FORTRANPATH = [modPath])
env.AppendUnique(F90PATH = [modPath])
env.AppendUnique(F77PATH = [modPath])
#add the includes needed by the framework
imageApiInc = os.path.join(buildDir,'components/iscesys/ImageApi/include')
dataCasterInc = os.path.join(buildDir,'components/iscesys/ImageApi/DataCaster/include')
lineAccessorInc = os.path.join(buildDir,'components/isceobj/LineAccessor/include')
stdOEInc =  os.path.join(buildDir,'components/iscesys/StdOE/include')
utilInc =  os.path.join(buildDir,'components/isceobj/Util/include')

env.AppendUnique(CPPPATH = [imageApiInc,dataCasterInc,lineAccessorInc,stdOEInc,utilInc])
env['HELPER_DIR'] = os.path.join(env['PRJ_SCONS_INSTALL'],'helper')
env['HELPER_BUILD_DIR'] = os.path.join(env['PRJ_SCONS_BUILD'],'helper')

#put the pointer function createHelp in the environment so it can be access anywhere
from configuration.buildHelper import createHelp
env['HELP_BUILDER'] = createHelp
#Create an env variable to hold all the modules added to the sys.path by default.
#They are the same as the one in in __init__.py in the same directory of this file
moduleList = []
installDir = env['PRJ_SCONS_INSTALL']
moduleList.append(os.path.join(installDir,'applications'))
moduleList.append(os.path.join(installDir,'components'))
env['ISCEPATH'] = moduleList
Export('env')


inst = env['PRJ_SCONS_INSTALL']


file = '__init__.py'
if not os.path.exists(file):
    fout = open(file,"w")
    fout.write("#!/usr/bin/env python3")
    fout.close()

env.Install(inst,file)
try:
    from subprocess import check_output
    svn_revision = check_output('svnversion').strip() or 'Unknown'
except ImportError:
    try:
        import popen2
        stdout, stdin, stderr = popen2.popen3('svnversion')
        svn_revision = stdout.read().strip()
        if stderr.read():
            raise Exception
    except Exception:
        svn_revision = 'Unknown'
except OSError:
    svn_revision = 'Unknown'

if not os.path.exists(inst):
    os.makedirs(inst)

fvers = open(os.path.join(inst,'version.py'),'w')

from release_history import release_version, release_svn_revision, release_date
fvers_lines = ["release_version = '"+release_version+"'\n",
               "release_svn_revision = '"+release_svn_revision+"'\n",
               "release_date = '"+release_date+"'\n",
               "svn_revision = '"+svn_revision+"'\n\n"]

fvers.write(''.join(fvers_lines))
fvers.close()

env.Alias('install',inst)
applications = os.path.join('applications','SConscript')
SConscript(applications)
components = os.path.join('components','SConscript')
SConscript(components)
defaults = os.path.join('defaults','SConscript')
SConscript(defaults)
library = os.path.join('library','SConscript')
SConscript(library)
contrib = os.path.join('contrib','SConscript')
SConscript(contrib)
