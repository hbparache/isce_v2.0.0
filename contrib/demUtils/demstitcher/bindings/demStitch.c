//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Copyright: 2010 to the present, California Institute of Technology.
// ALL RIGHTS RESERVED. United States Government Sponsorship acknowledged.
// Any commercial use must be negotiated with the Office of Technology Transfer
// at the California Institute of Technology.
// 
// This software may be subject to U.S. export control laws. By accepting this
// software, the user agrees to comply with all applicable U.S. export laws and
// regulations. User has the responsibility to obtain export licenses,  or other
// export authority as may be required before exporting such information to
// foreign countries or providing access to foreign persons.
// 
// Installation and use of this software is restricted by a license agreement
// between the licensee and the California Institute of Technology. It is the
// User's responsibility to abide by the terms of the license agreement.
//
// Author: Giangi Sacco
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




#include <stdio.h>
#include <stdlib.h>

void swap2Bytes(short * in, short * out, int numEl)
{
    int i = 0;
    for(i = 0; i < numEl; ++i)
    {
       out[i] = (in[i] & 0xFF00) >> 8 | 
        ( in[i] & 0x00FF) << 8;
    }
}
int concatenateDem(char ** filenamesIn, int * numFilesV,char * filenameOut, int * samples, int * swap)
{
    int GlobalNumSamples = (*samples);
    char ** GlobalInputFilenames = filenamesIn;
    char * GlobalOutputFilename = filenameOut;
    // this has two value [numRow,numCol] i.e. the number of files along the rows and the number of files along the column. 
    int * GlobalNumFiles = numFilesV;
    //number of samples in the file
    int GlobalNeedSwap = (*swap);
    int i = 0;
    int j = 0;
    int k = 0;
    int l = 0;
    long int pos = 0;
    FILE * fout;
    

    int numFiles = GlobalNumFiles[0]*GlobalNumFiles[1];
    FILE ** fin = malloc(sizeof(FILE *)*numFiles);
    // load all the images in one buffer, they are small anyway
    short * inbuf = malloc(sizeof(short)*GlobalNumSamples*GlobalNumSamples*GlobalNumFiles[0]*GlobalNumFiles[1]);
    //beacuse hte edge overlap we excluse the very last column to the right and the very last row to the bottom
    short * outbuf = malloc(sizeof(short)*((GlobalNumSamples - 1)*GlobalNumFiles[0])*((GlobalNumSamples - 1)*GlobalNumFiles[1]));
    
    if(fin == NULL)
    {
        fprintf(stderr,"Cannot allocate  file pointers for stitching.\n");
        return 1; 
    }
    fout = fopen(GlobalOutputFilename,"w");
    if(fout == NULL)
    {
        fprintf(stderr,"Cannot open DEM output file %s for writing.\n",GlobalOutputFilename);
        return 1;
    }
    //load all files
    for(i = 0; i < numFiles; ++i)
    {
        fin[i] = fopen(GlobalInputFilenames[i],"r");
        if(fin[i] == NULL)
        {
            fprintf(stderr,"Cannot open DEM file %s for reading.\n",GlobalInputFilenames[i]);
            return 1; 

        }
        //read the all file
        fread(&inbuf[pos],sizeof(short),GlobalNumSamples*GlobalNumSamples,fin[i]);
        fclose(fin[i]);
        pos += GlobalNumSamples*GlobalNumSamples;
    }
    if(GlobalNeedSwap == 1)
    {
        short * tmpbuf = malloc(sizeof(short)*GlobalNumSamples*GlobalNumSamples*GlobalNumFiles[0]*GlobalNumFiles[1]);
        int numEl = GlobalNumSamples*GlobalNumSamples*GlobalNumFiles[0]*GlobalNumFiles[1];
        swap2Bytes(inbuf, tmpbuf, numEl);
        free(inbuf);
        inbuf = tmpbuf;

    }
    pos = 0;
    for(i = 0; i < GlobalNumFiles[0]; ++i)
    {
        for(l = 0; l < GlobalNumSamples - 1; ++l)
        {
            for(j = 0; j < GlobalNumFiles[1]; ++j)
            {
                for(k = 0; k < GlobalNumSamples - 1; ++k)
                {
                    outbuf[pos] = inbuf[k + l*GlobalNumSamples + j*GlobalNumSamples*GlobalNumSamples +i*GlobalNumSamples*GlobalNumSamples*GlobalNumFiles[1]]; 
                    ++pos;
                }

            }
        }
    }
    fwrite(outbuf,sizeof(short),pos,fout);
    fclose(fout);
    free(fin);
    free(inbuf);
    free(outbuf);
    return 0;

}
/*
int main(int argc, char ** argv)
{
    short int bufin[121];
    int  dim[2] = {2,3};
    int samp = 11;
    char * output = "outDemTest";
    int i,j,v,k;
    FILE * fp;
    k = 0;
    for(i = 0; i < 11; ++i)    
    {
        for(j = 0; j < 11; ++j)    
        {
            bufin[k] = k;

        if((k%11) == 0)
            printf("\n");
            printf("%3d ",k);
            ++k;
        }
    }
    printf("\n");
    fp = fopen("testFileDem","w");
    fwrite(bufin,sizeof(short),121,fp);
    fclose(fp);
    char ** filein = malloc(sizeof(char *)*6);
    for(i = 0; i < 6; ++i)
    {

        filein[i] = "testFileDem";
    }
    setNumSamples(&samp);
    setOutputFilename(output);
    setInputFilenames(filein);
    setNumFiles(dim);
    concatenateDem();
}
*/

