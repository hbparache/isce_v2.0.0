#!/usr/bin/env python3


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2011 to the present, California Institute of Technology.
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




import xml.etree.ElementTree as ET
from collections import UserDict

class OrderedDict(UserDict):
    def __init__(self, adict = None):
        self._keys = []
        UserDict.__init__(self, adict)

    def __delitem__(self, key):
        UserDict.__delitem__(self, key)
        self._keys.remove(key)

    def __setitem__(self, key, item):
        UserDict.__setitem__(self, key, item)
        if key not in self._keys: self._keys.append(key)

    def clear(self):
        UserDict.clear(self)
        self._keys = []

    def copy(self):
        adict = UserDict.copy(self)
        adict._keys = self._keys[:]
        return adict

    def items(self):
        return zip(self._keys, self.values())

    def keys(self):
        return self._keys

    def popitem(self):
        try:
            key = self._keys[-1]
        except IndexError:
            raise KeyError('dictionary is empty')

        val = self[key]
        del self[key]

        return (key, val)

    def setdefault(self, key, failobj = None):
        UserDict.setdefault(self, key, failobj)
        if key not in self._keys: self._keys.append(key)

    def update(self, adict):
        UserDict.update(self, adict)
        for key in adict.keys():
            if key not in self._keys: self._keys.append(key)

    def values(self):
        return map(self.get, self._keys)



def dict_to_xml(adict,file):
    a = ET.Element('')  # something to hang nodes on
    a = dict_to_et(a,adict)
    et = a.getchildren()[0]
    indent(et)
    tree = ET.ElementTree(et)
    tree.write(file)

def dict_to_et(node,adict):
    for key, val in adict.items():
        if isinstance(val,UserDict) or isinstance(val,dict):
            subnode = ET.Element(key)
            node.append(subnode)
            subnode = dict_to_et(subnode,val)
        else:
            subnode = ET.Element(key)
            node.append(subnode)
            subnode.text = str(val)
    return node

def indent(elem, depth = None,last = None):
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
            indent(elem[i],depth,lastCp)
            
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


