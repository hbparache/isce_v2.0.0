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




import os, errno, itertools
from .OrderedDict import OrderedDict
from io import StringIO

HEADER = "\n%s\n    %%s\n%s\n" % ("#"*100, '-'*100)
FOOTER = "#"*100
MAX_LIST_SIZE = 20

class Catalog(OrderedDict):
    # This bigArrayNum variable is used to ensure that big array files are
    # unique on disk. Some components that use the Catalog class are used
    # multiple times.
    bigArrayNum = 0

    def __init__(self, name, nodePath=None):
        OrderedDict.__init__(self)
        self.name = name
        if nodePath is None:
            self.fullName = name
        else:
            self.fullName = '.'.join(nodePath)
        return

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for other_k, other_v in other.items():
            try:
                self_v = self[other_k]
            except KeyError as e:
                return False
            if not (self_v == other_v):
                return False
        return True

    def addItem(self, key, value, node):
        """
        Adds given key/value pair to the specified node. If the node does not
        exist, it is created.
        """
        nodePath = node.split('.')
        self._addItem(key, value, nodePath)

    def hasNode(self, node):
        """
        Indicates whether a node exists in this catalog (such as "foo.bar.baz")
        """
        if not isinstance(node,str):
            raise TypeError("'node' must be a string")
        nodeList = node.split('.')
        return _hasNodes(nodeList)

    def _hasNodes(self, nodeList):
        catalog = self
        for node in nodeList:
            if (node not in catalog) or (not isinstance(catalog[node], Catalog)):
                return False
            catalog = catalog[node]
        return True

    def addAllFromCatalog(self, otherCatalog):
        """Adds all the entries from the other catalog into this catalog."""
        if not isinstance(otherCatalog, Catalog):
            raise TypeError("'otherCatalog' must be of type Catalog")
        self._addAllFromCatalog(otherCatalog, [])

    def _addAllFromCatalog(self, otherCatalog, nodePath):
        for k, v in otherCatalog.items():
            if isinstance(v, Catalog):
                nodePath.append(v.name)
                self._addAllFromCatalog(v, nodePath)
                nodePath.pop()
            else:
                self._addItem(k, v, nodePath)

    def addInputsFrom(self, obj, node):
        """
        Given an object, attempts to import its dictionaryOfVariables attribute
        into this catalog under the given node.
        """
        if not hasattr(obj, 'dictionaryOfVariables'):
            raise AttributeError(
                "The object of type {} ".format(obj.__class__.__name__)
                 +  "does not have a dictionaryOfVariables attribute!")
        nodePath = node.split('.')
        for k, v in obj.dictionaryOfVariables.items():
            attr = v[0].replace('self.', '', 1)
            self._addItem(k, getattr(obj, attr), nodePath)
        if 'constants' in iter(list(obj.__dict__.keys())):
            for k, v in list(obj.constants.items()):
                self._addItem(k, v, nodePath)

    def addOutputsFrom(self, obj, node):
        """
        Given an object, attempts to import its dictionaryOfOutputVariables
        attribute into this catalog under the given node.
        """
        if not hasattr(obj, 'dictionaryOfOutputVariables'):
            raise AttributeError("The object of type '%s' does not have a " + \
                                 "dictionaryOfOutputVariables attribute!" % obj.__class__.__name__)
        nodePath = node.split('.')
        for k, v in obj.dictionaryOfOutputVariables.items():
            attr = v.replace('self.', '', 1)
            self._addItem(k, getattr(obj, attr), nodePath)

    def _addItem(self, key, value, nodePath):
        catalog = self
        partialPath = []
        for node in nodePath:
            partialPath.append(node)
            # Instantiate a new catalog if the node does not already exist
            if node not in catalog:
                catalog[node] = Catalog(node, partialPath)
            catalog = catalog[node]
        # Just record the file info if this value is actually a large array
        catalog[key] = self._dumpValueIfBigArray(key, value, nodePath)

    def _dumpValueIfBigArray(self, key, v, nodePath):
        """Checks to see if the value is a list greater than the defined length threshhold. If so,
        dump the array to a file and return a string value indictating the file name. Otherwise,
        return the normal value."""
        if self._isLargeList(v):
            # Make the catalog directory if it doesn't already exist
            try:
                os.makedirs('catalog')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    print("Couldn't create directory, 'catalog'! Please check your permissions.")
                    raise
            fileName = 'catalog/%s.%s.%03i' % ('.'.join(nodePath), key, Catalog.bigArrayNum)
            Catalog.bigArrayNum += 1
            f = open(fileName, 'w')
            self.writeArray(f, v)
            f.close()
            v = fileName
        return v

    def writeArray(self, file, array):
        """Attempts to output arrays in a tabular format as neatly as possible. It tries
        to determine whether or not it needs to transpose an array based on if an array is
        multidimensional and if each sub-array is longer than the main array."""
        # The arrya is guaranteed to be > 0 by the caller of this method
        multiDim = isinstance(array[0], list) or isinstance(array[0], tuple)
        # 'transpose' the array if each element array is longer than the main array
        # this isn't fool proof and might produce incorrect results for short multi-dim
        # arrays, but it work in practice
        if multiDim and len(array[0]) > len(array):
            array = zip(*array)
        for e in array:
            if multiDim:
                e = '\t'.join(str(x) for x in e)
            else:
                e = str(e)
            file.write("%s\n" % e)


    def _isLargeList(self, l):
        """This handles the fact that a list might contain lists. It returns True if the list
        itself or any of its sublists are longer than MAX_LIST_SIZE. If 'l' is not a list,
        False is returned. This method does assume that all sublists will be the same size."""
        while (isinstance(l, list) or isinstance(l, tuple)) and len(l) > 0:
            if len(l) > MAX_LIST_SIZE:
                return True
            l = l[0]
        return False


    def printToLog(self, logger, title):
        """Prints this catalog to the given logger, one entry per line.
        Example output line: foo.bar = 1"""
        file = StringIO()
        file.write(HEADER % title)
        self._printToLog(file, self)
        file.write(FOOTER)
        logger.info(file.getvalue())

    def _printToLog(self, file, catalog):
        for k, v in catalog.items():
             if isinstance(v, Catalog):
                  self._printToLog(file, v)
             else:
                  file.write("%s.%s = %s\n" % (catalog.fullName, k, str(v)))

    def renderXml(self, file=None, nodeTag=None, elementTag=None):
        if not file:
           file = self.fullName+'.xml'

        adict = {self.fullName:self}

#        from isceobj.XmlUtil import xmlUtils as xmlu
        dict_to_xml(adict,file,nodeTag=nodeTag,elementTag=elementTag)




import xml.etree.ElementTree as ET
from collections import UserDict

def dict_to_xml(adict,file,nodeTag=None,elementTag=None):
    a = ET.Element(nodeTag)  # something to hang nodes on
    a = dict_to_et(a,adict,nodeTag,elementTag)
    et = a.getchildren()[0]
    indent(et)
    tree = ET.ElementTree(et)
    tree.write(file)

def dict_to_et(node,adict,nodeTag,elementTag):
    for key, val in adict.items():
        if isinstance(val,UserDict) or isinstance(val,dict):
            if nodeTag:
               subnode = ET.Element(nodeTag)
               node.append(subnode)
               name = ET.Element('name')
               subnode.append(name)
               name.text = str(key)
            else:
               subnode = ET.Element(key)
               node.append(subnode)
            subnode = dict_to_et(subnode,val,nodeTag,elementTag)
        else:
            if elementTag:
               subnode = ET.Element(elementTag)
               node.append(subnode)
               name = ET.Element('name')
               subnode.append(name)
               name.text = str(key)
               value = ET.Element('value')
               subnode.append(value)
               value.text = str(val).replace('\n', '\\n')
            else:
               lmnt = ET.Element(key)
               node.append(lmnt)
               lmnt.text = str(val).replace('\n', '\\n')
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
