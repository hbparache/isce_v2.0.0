#ifndef InterleavedAccessor_h
#define InterleavedAccessor_h

#ifndef MESSAGE
#define MESSAGE cout << "file " << __FILE__ << " line " << __LINE__ << endl;
#endif
#ifndef ERR_MESSAGE
#define ERR_MESSAGE cout << "Error in file " << __FILE__ << " at line " << __LINE__  << " Exiting" <<  endl; exit(1);
#endif

#include <stdlib.h>
#include <string>
#include <fstream>
using namespace std;

class InterleavedAccessor
{
    public:
        InterleavedAccessor(){
            EofFlag = 0;
            Data = NULL;
                            }
        virtual ~InterleavedAccessor(){}
        /**
         * Get the numEl pixels  from the Fin stream starting from the position (row,col). The number of rows and columns are zero based.
         **/
        virtual void getData(char * buf,int row, int col, int & numEl) = 0;
        virtual void getDataBand(char *buf,int row, int col, int &numEl, int band) = 0;
        virtual void setData(char * buf,int row, int col, int  numEl) = 0;
        virtual void setDataBand(char * buf, int row, int col, int numEl, int band) = 0;
        void getStreamAtPos(char * buf,int & pos,int & numEl);
        void setStreamAtPos(char * buf,int & pos,int & numEl);
        void getStream(char * buf,int & numEl);
        void setStream(char * buf,int numEl);
        void finalize();
        void alloc(int numLines);
        void init(string filename,string accessMode,int sizeV,int Bands, int LineWidth);
        void setLineWidth(int lw){LineWidth = lw;}
        void setDataSize(int ds){SizeV = ds;}
        void setBands(int bd){Bands = bd;}
        int getLineWidth(){return LineWidth;}
        int getDataSize(){return SizeV;}
        int getBands(){return Bands;}
        int getFileLength();
        int getEofFlag(){return EofFlag;}
        void createFile(int numberOfLine);
        void setAccessMode(string accessMode);
        string getAccessMode(){return AccessMode;};
        void openFile(string filename, string accessMode, fstream & fd);
        fstream & getFileObject(){return FileObject;}
        void rewindAccessor();


    protected:
        /**
         * Name associated with the image file.
         *
         **/
        string Filename;
        /**
         * Stream associated with the image file.
         *
         **/
        fstream  FileObject;
        /**
         * Size of the DataType.
         **/
        int SizeV;

        /**
         * Number of bands for the adopted interleaved scheme.
         **/
        int Bands;

        /**
         * Number of pixels per line.
         **/
        int LineWidth;

        /**
         * Number of  lines.
         **/
        int NumberOfLines;

        /**
         * Access mode of the underlaying file object.
         **/
        string AccessMode;
        /**
         * Flag that is set to 1 when the EOF is reached. 
         **/

        int EofFlag;
        /**
         * Flag that is set to 1 when the good() stream method returns false. 
         **/

        int NoGoodFlag;

        char * Data;

};

#endif //InterleavedAccessor_h
