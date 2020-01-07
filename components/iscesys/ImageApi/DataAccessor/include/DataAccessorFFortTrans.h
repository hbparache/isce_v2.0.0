
#ifndef DataAccessorFFortTrans_h
#define DataAccessorFFortTrans_h

	#if defined(NEEDS_F77_TRANSLATION)

		#if defined(F77EXTERNS_LOWERCASE_TRAILINGBAR)
			#define setLineSequential_f setlinesequential_
                        #define setLineSequentialBand_f setlinesequentialband_
			#define setSequentialElements_f setsequentialelements_
			#define setLine_f setline_
                        #define setLineBand_f setlineband_
			#define setStream_f setstream_
			#define setStreamAtPos_f setstreamatpos_
			#define getLineSequential_f getlinesequential_
                        #define getLineSequentialBand_f getlinesequentialband_
			#define getSequentialElements_f getsequentialelements_
			#define getStream_f getstream_
			#define getStreamAtPos_f getstreamatpos_
			#define getLine_f getline_
                        #define getLineBand_f getlineband_
	        #define initSequentialAccessor_f initsequentialaccessor_
		#else
			#error Unknown traslation for FORTRAN external symbols
		#endif

	#endif

#endif DataAccessorFFortTrans_h
