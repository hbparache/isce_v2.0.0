#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

#ifndef SUN_MACRO
static double nintarg;
#define nint(a) ( ((nintarg=(a)) >= 0.0 )?(int)(nintarg+0.5):(int)(nintarg-0.5) )
#define aint(a) ((double)(int)(a))
#define log2(a) (log(a)/.693147181)
#define exp2(a) (pow(2.0,a))
#define SUN_MACRO	1
#endif

#define MAX_STATE 5		/* maximum number of state vectors in the SLC parameter file */
#define MAR       3    		/* range offset fit linear coefficients in a1 + a2*r + a3*az */
#define MAAZ      3    		/* azimuth offset fit linear coefficients in a1 + a2*r + a3*az */

#ifndef STRUCTURES
typedef struct {float re,im;} fcomplex;
typedef struct{double x,y,z;} VEC;	/* vector structure cartesian (X,Y,Z)*/
typedef struct{double t,c,n;} VEC_TCN;	/* vector structure (Track, Cross-Track, Normal) */
typedef struct{			/* state vector structure */
   VEC pos;			/* position vector */
   VEC vel;			/* velocity vector */
} STATE;			/* state vector */
typedef struct{
  int mjd;		/* modified Julian date, which is (julian date - 2433282.5) example: 1.1.1990 = 14610 */
  int utc;		/* time in msec since midnight UTC */
  int orb_num;		/* orbit number */
  VEC pos;		/* sensor position (xyz) Conventional Terrestrial System (km) */
  VEC vel;		/* sensor velocity (xyz) Conventional Terrestrial System (km/sec) */
  int TAI_UTC_delta;	/* value in seconds of the difference between the Internation Atomic Time and UTC */
} ORRM;
typedef double **MAT;
#define STRUCTURES 	1
#endif

typedef struct{double re,im;} dcomplex;	/* double precision complex data type */ 
typedef struct{float az,cr;} Slope; 	/* azimuth,range slope */     

typedef struct{			/* single look complex image parameters */
  char title[128];		/* ascii string with title of the scene */
  char date[25];		/* date in form: YYYY MM DD hh mm ss.ttt UTC */
  double t0,t1,t2;		/* time of image start, center, end  UTC seconds since start of day */
  int hdrsz;			/* header size in bytes for each line */
  int nr;			/* number of range pixels/line */
  int naz;			/* number of range lines in the scene */
  double cen_line, cen_pix;	/* line  and pixel of the center of the image */
  double c_lat, c_lon;		/* latitude, longitude of scene center in decimal degrees */
  double c_head;		/* subsatellite track heading at mid azimuth */
  double rps;			/* slant range SLC pixel spacing in meters */
  double azps;			/* azimuth along SLC track pixel spacing (meters) */
  double r0,r1,r2;		/* near, center, far slant range of image (meters) */
  double c_inc;			/* incidence angle at the center of the scene (deg.) */
  double fcen;			/* radar carrier center frequency (Hz) */
  double fadc;			/* sample rate  of radar analog to digital converter (Hz) */
  double chbw;			/* radar range chirp bandwidth (Hz) */
  double prf;			/* radar pulse repetition frequency (Hz) */
  double azpbw;			/* 3 dB azimuth processing bandwidth (Hz) */
  double f0,f1,f2,f3;		/* doppler centroid polynomial coefficients f0 + f1*(r-r1) + f2*(r-r1)**2 + f3*(r-r1)**3
				   (r is the slant range and r1 is the slant range at the center of the image */
  double rdist,re_cen;		/* distance of sensor from earth center at center scene, 
				   center scene geocentric radius (m)*/
  double el_major, el_minor;	/* earth ellipsoid semi-major, semi-minor axises (m) */
  int nstate;			/* number of state vectors */
  double t_state;		/* UTC time (sec) since start of day for first state vector */
  double tis;			/* time interval between state vectors (s) */
  STATE state[MAX_STATE];	/* maximum of MAX_STATE state vectors (X,Y,Z) CTS */  
} SLC_PAR;

typedef struct{			/* interferogram parameters and SLC offset data */
  char title[128];		/* ascii string with title of interferogram */
  int initr,initaz;		/* integer offsets in complex pixels, range and azimuth */
  int nofstr,npr;		/* #points offset from start, #points range to process */
  int rstr,rend,nr,rsp;		/* starting range sample, ending range sample, 
				number of points in range for offset estimates, range offset sample spacing */
  int azstr,azend,naz,azsp;	/* starting azimuth, ending azimuth, 
      				   number of azimuth points for offset estimates, azimuth offset sample spacing */
  int rwin,azwin;		/* maximum sizes of window in range, azimuth to estimate offset at each point */
  double thres;			/* fringe SNR threshold to save offset estimate or discard */
  double rpoly[MAR];		/* range offset polynomial as a function of range and azimuth; range coordinate is relative to
				   interferogram starting range pixel (nofstr), azimuth coordinate is relative to SLC-1 */
  double azpoly[MAAZ];		/* azimuth offset polynomial as a function of range in azimuth; range coordinate is relative to
				   interferogram starting range pixel (nofstr), azimuth coordinate is relative to SLC-1 */
  int lbegin;			/* starting line in interferogram (relative to start of SLC-1) */
  int nls;			/* number of interfogram lines */
  int nr_int;			/* width of interferogram (samples) */
  int nrb;			/* offset from start of each line for the first valid interferogram pixel */
  int nrps;			/* number of valid slant range pixels in the interferogram */
  int rlks,azlks;		/* number of interferometric looks in range and azimuth */
  double rps_int, azps_int; 	/* interferogram sample spacing (meters) in slant range and azimuth */
  double rps_res,azps_res;  	/* true ground range and azimuth spacing (meters) in resampled height map */
  double grg_start;		/* starting ground range relative to center swath at altitude=0.0 */
  int ngrg;			/* # samples in the cross-track direction */
} OFF_PAR;

typedef struct{
  /*****************************************************************************************
      		State vector estimate of baseline at center of SLC-1, 
		baseline velocity, (expressed in TCN) (m)   
  ******************************************************************************************/
  VEC_TCN base_orb;
  VEC_TCN bdot_orb;
  /*****************************************************************************************
        	Baseline at center of SLC-1, baseline velocity, (expressed in TCN) (m)
		using L.S. fitting of the baseline parameters from tiepoints 
  *******************************************************************************************/
  VEC_TCN base;
  VEC_TCN bdot;
  /******************************************************************************************/
  double phc;		/* interferometric phase constant estimated using Least Squares model fitting of the 
			   baseline from tiepoints (radians) */
} BASELINE;

typedef struct{
  int		irg;	/* slant range pixel position */
  int		iaz;	/* azimuth pixel position */
  double 	alt;	/* altitude for point relative to reference ellipsoid (m)*/
  double 	ph;	/* unwrapped measured phase (radians) */
  double	phr;	/* phase with range phase added in (radians) */
  double	lat;    /* latitude of point (deg.) */
  double	lng;    /* longitude of point (deg.) */
  double	ti;	/* time relative to center of scene (s) */
  double	rg;	/* slant range (m) */
  double	th;	/* look angle (relative to TCN) (radians) */
  VEC_TCN       base;	/* baseline expressed in TCN */
  VEC_TCN	lv;	/* look-vector for GCP expressed in TCN */
 } GCP;
