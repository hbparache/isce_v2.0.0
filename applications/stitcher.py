#!/usr/bin/env python3 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2012 to the present, California Institute of Technology.
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
import isce
import logging
import logging.config
from iscesys.Component.Application import Application
class Stitcher(Application):
    def main(self):
        # prevent from deleting local files
        if(self.demStitcher._useLocalDirectory):
            self.demStitcher._keepAfterFailed = True
            self.demStitcher._keepDems = True
        # is a metadata file is created set the right type
        if(self.demStitcher._meta == 'xml'):
            self.demStitcher.setCreateXmlMetadata(True)
        elif(self.demStitcher._meta == 'rsc'):
            self.demStitcher.setCreateRscMetadata(True)
        # check for the action to be performed
        if(self.demStitcher._action == 'stitch'):
            if(self.demStitcher._bbox):
                lat = self.demStitcher._bbox[0:2]
                lon = self.demStitcher._bbox[2:4]
                if (self.demStitcher._outputFile is None):
                    self.demStitcher._outputFile = self.demStitcher.defaultName(self.demStitcher._bbox)
    
                if not(self.demStitcher.stitchDems(lat,lon,self.demStitcher._source,self.demStitcher._outputFile,self.demStitcher._downloadDir, \
                        keep=self.demStitcher._keepDems)):
                    print('Could not create a stitched DEM. Some tiles are missing')
                else:
                    if(self.demStitcher._correct):
                        width = self.demStitcher.getDemWidth(lon,self.demStitcher._source)
                        self.demStitcher.correct(os.path.join(self.demStitcher._dir,self.demStitcher._outputFile), \
                                     self.demStitcher._source,width,min(lat[0],lat[1]),min(lon[0],lon[1]))
                        #self.demStitcher.correct(self.demStitcher._output,self.demStitcher._source,width,min(lat[0],lat[1]),min(lon[0],lon[1]))
            else:
                print('Error. The --bbox (or -b) option must be specified when --action stitch is used')
                raise ValueError
        elif(self.demStitcher._action == 'download'):
            if(self.demStitcher._bbox):
                lat = self.demStitcher._bbox[0:2]
                lon = self.demStitcher._bbox[2:4]
                self.demStitcher.getDemsInBox(lat,lon,self.demStitcher._source,self.demStitcher._downloadDir)
            #can make the bbox and pairs mutually esclusive if replace the if below with elif
            if(self.demStitcher._pairs):
                self.demStitcher.downloadFilesFromList(self.demStitcher._pairs[::2],self.demStitcher._pairs[1::2],self.demStitcher._source,self.demStitcher._downloadDir) 
            if(not (self.demStitcher._bbox or self.demStitcher._pairs)):
                print('Error. Either the --bbox (-b) or the --pairs (-p) options must be specified when --action download is used')
                raise ValueError
        
        else:
            print('Unrecognized action -a or --action',self.demStitcher._action)
            return
    
        if(self.demStitcher._report):
            for k,v in self.demStitcher._downloadReport.items():
                print(k,'=',v)
    
    def _facilities(self):
        """
        Define the user configurable facilities for this application.
        """
        self.demStitcher = self.facility(
            'demStitcher',
            public_name='demStitcher',
            module='contrib.demUtils',
            factory='createDemStitcher',
            args=('iscestitcher',),
            mandatory=False,
            doc=(
                "Object that based on the frame bounding boxes creates a DEM"
                )
            )
    def help(self):
        print("\nUsage: stitcher.py input.xml\n")
        print("Description of properties:\n")
        for k,v in self.demStitcher.descriptionOfVariables.items():
            print("-",k,":",v['doc'])
            print()
        print("NOTE: if you don't want to store your password in a file you can run it as\n" +\
              "'stitcher.py input.xml sticher.demStitcher.username=yourUsername\n" +\
              "sticher.demStitcher.password=yourPassword'\n\n" )
    
    family = 'stitcher'            
    def __init__(self,family = '', name = ''):
        super(Stitcher, self).__init__(family if family else  self.__class__.family, name=name)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and (sys.argv.count('-h') or sys.argv.count('--help')):
        if (sys.argv.count('-h')):        
            sys.argv.remove('-h') #remove it form sys.argv 
        elif (sys.argv.count('--help')):        
            sys.argv.remove('--help')
        #need to remove the -h or --help otherwise the parser thinks is  a file
        ds = Stitcher()
        ds.help()
    else:
        ds = Stitcher()
        ds.run()
