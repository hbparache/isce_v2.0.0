#!/usr/bin/env python3 

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





from __future__ import print_function
import sys
import os
import math
from iscesys.Compatibility import Compatibility
Compatibility.checkPythonVersion()
from iscesys.Component.Component import Component
import xml.etree.ElementTree as ET
from iscesys.DictUtils.DictUtils import DictUtils as DU
import logging
class XmlDumper:


    def addProperty(self,parent,name,value,propMisc):
        child = ET.SubElement(parent,"property",name=name)
        ET.SubElement(child, 'value').text = str(value)
        if not propMisc == None:
            for pkey in self._propertyKeys:
                if pkey in propMisc:
                    ET.SubElement(child, pkey).text = str(propMisc[pkey])
    def addComponent(self,parent,dictIn,factDict = None,miscDict = None):
        for key,val in dictIn.items():
            
            if (not factDict == None) and key in factDict:#check in the key is in the factory dictionary. that means that is a component
                comp = factDict[key]
                child = ET.SubElement(parent,"component",name=key)
                for ckey in self._componentKeys:
                    if ckey in comp:
                        ET.SubElement(child,ckey).text = str(comp[ckey])
                valMisc = None
                if (not miscDict == None) and key in miscDict:
                    valMisc = miscDict[key]
                self.addComponent(child,val,comp,valMisc)
                
            else:#is a property
                propMisc = None
                if not miscDict == None:
                    if key in miscDict:
                        propMisc = miscDict[key]
                self.addProperty(parent,key,val,propMisc)
                
    def indent(self,elem, depth = None,last = None):
        if depth == None:
            depth = [0]
        if last == None:
            last = False
        tab = ' '*4
        if(len(elem)):
            depth[0] += 1
            elem.text = '\n' + (depth[0])*tab
            lenEl = len(elem)
            lastCp = False
            for i in range(lenEl):
                if(i == lenEl - 1):
                    lastCp = True
                self.indent(elem[i],depth,lastCp)
            if(not last):
                elem.tail = '\n' + (depth[0])*tab
            else:
                depth[0] -= 1
                elem.tail = '\n' + (depth[0])*tab
        else:
            if(not last):
                elem.tail = '\n' + (depth[0])*tab
            else:
                depth[0] -= 1
                elem.tail = '\n' + (depth[0])*tab
   
    def dump(self,outfile,propDict,factDict = None, miscDict = None,firstTag = None):
        if firstTag == None:
            firstTag = "input"
        root = ET.Element(firstTag)
        self.addComponent(root,propDict,factDict,miscDict)
        self.indent(root)
        etObj = ET.ElementTree(root)
        fp = open(outfile,'wb')
        etObj.write(fp)
        fp.close()

    def __getstate__(self):
        d = dict(self.__dict__)
        del d['logger']
        return d
    def __setstate__(self,d):
        self.__dict__.update(d)
        self.logger = logging.getLogger('isce.iscesys.Dumpers.XmlDumper')
    def __init__(self):
        self._filetypes = ['xml'] # add all the types here
        self.logger = logging.getLogger('isce.iscesys.Dumpers.XmlDumper')
        self._componentKeys = ['factorymodule','factoryname','args','kwargs','doc']
        self._propertyKeys = ['doc','units']

def main(argv):
    from iscesys.Parsers.Parser import Parser
    import pdb
    pdb.set_trace()
    PA = Parser()
    (propDict,factDict,miscDict,opts) = PA.commandLineParser(argv)
    XD = XmlDumper()
    outfile = "thisIsADumpTest.xml"
    firstTag = 'input' 
    XD.dump(outfile,propDict,factDict, miscDict,firstTag)
    (propDict1,factDict1,miscDict1,opts) = PA.commandLineParser([outfile])

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
