#include <cstdlib>
#include <iostream>
#include <fstream>
#include <string.h>
#include <vector>
#include <sstream>
#include <math.h>
#include <sstream>

using namespace std;

const float PI(3.14159);

// standard autocorrelation loop

float FormFactor(float q,float atomZ){
	float FF;
	float qo = (q*q) / (4*4*PI*PI);
	if (int(atomZ) == 1){
		FF = 0.493002*exp(-10.5109*qo);
		FF+= 0.322912*exp(-26.1257*qo);
		FF+= 0.140191*exp(-3.14236*qo);
		FF+= 0.040810*exp(-57.7997*qo);
		FF+= 0.003038;
		}
	else if (int(atomZ) == 8){
		FF = 3.04850*exp(-13.2771*qo);
		FF+= 2.28680*exp(-5.70110*qo);
		FF+= 1.54630*exp(-0.323900*qo);
		FF+= 0.867000*exp(-32.9089*qo);
		FF+= 0.2508;
		}
	else if (int(atomZ) == 26){
		FF = 11.7695*exp(-4.7611*qo);
		FF+= 7.35730*exp(-0.307200*qo);
		FF+= 3.52220*exp(-15.3535*qo);
		FF+= 2.30450*exp(-76.8805*qo);
		FF+= 1.03690;
		}
	else if (int(atomZ) == 79){
		FF = 16.8819*exp(-0.4611*qo);
		FF+= 18.5913*exp(-8.6216*qo);
		FF+= 25.5582*exp(-1.4826*qo);
		FF+= 5.86*exp(-36.3956*qo);
		FF+= 12.0658;
		}
	else /*approx with Nitrogen*/
		FF = 12.2126*exp(-0.005700*qo);
		FF+= 3.13220*exp(-9.89330*qo);
		FF+= 2.01250*exp(-28.9975*qo);
		FF+= 1.16630*exp(-0.582600*qo);
		FF+= -11.529;
	return FF;
	}

int main(int argc, char * argv[]){

FILE * pFile = fopen(argv[1],"r");// open coordinate file
int coorPerShot = atoi(argv[2]);// how many coordinates per shot
int numberShots = atoi(argv[3]);// how many shots to read
int Nphi = atoi(argv[4]); // number of bins around diffraction ring
float deltaPhi = 2*PI / Nphi;
int cleanUp = atoi(argv[5]);

int numOutFileNames = atoi(argv[6]);//output file directory
FILE * pOutFile[numOutFileNames];
for(int i=7;i<7+numOutFileNames;i++)
	pOutFile[i-7] = fopen(argv[i],"ab");

//float w; // weight for the scattering average
float * binData = new float[coorPerShot];//open an array for the coordinates
float * binDataQA = new float[Nphi];//create an array for the scattering
float * binDataQB = new float[Nphi];//create an array for the scattering

vector<float> THETA,Q; vector<string> QSTRING;
for(int i=7+numOutFileNames;i<argc;i+=3){
	THETA.push_back( atof(argv[i]) );
	Q.push_back( atof(argv[i+1]) );
	QSTRING.push_back( string(argv[i+2]) );
	}

//create output file name
//open output files
//FILE * pOutFile = fopen(outFileName.c_str(),"ab");

int n(0);
while(n<numberShots){
//	read coordinates into binData
	//fread(&w, 4, 1, pFile); // first float is the weight
	fread(binData,4,coorPerShot,pFile);
	for(int i=0;i < Q.size();i++){
		float theta = THETA[i]; // angle on detector
		float cosTheta = cos(theta);
		float q = Q[i]; // magnitude of q vector
		float qZ = q*sin(theta); // z-component of q vector
		string qName = QSTRING[i]; // name of scattering output file

		float phi(0);
		int phiIndex(0);
		while (phi < 2*PI){
			float qX = q*cosTheta*cos(phi);
			float qY = q*cosTheta*sin(phi);
	//		sums for the complex exponential
			float sum1(0),sum2(0); // sum1 = real part, sum2 = im part
			int m(0); // atom coordinate index
			while(m<coorPerShot){
	//			get the position vector of the atom in the shot
				float rX = binData[m]; // atomX
				float rY = binData[m+1]; // atomY
				float rZ = binData[m+2]; // atomZ
				float A = binData[m+3];
	//			phase angle
				float phase = rX*qX + rY*qY + rZ*qZ;
				//sum1 += FormFactor(q,A)*cos(phase);
				//sum2 += FormFactor(q,A)*sin(phase);
				sum1 += A*cos(phase);
				sum2 += A*sin(phase);
				m+=4;
				}
			binDataQA[phiIndex] = sum1;
			binDataQB[phiIndex] = sum2;
			
			phi += deltaPhi;
			phiIndex += 1;
			}
	//	save scattering from the shot
		fwrite(binDataQA,4,Nphi,pOutFile[i]);
		fwrite(binDataQB,4,Nphi,pOutFile[i]);
		}
	n += 1;
	}

for(int i=0; i<numOutFileNames;i++)
	fclose(pOutFile[i]);

delete [] binData;
delete [] binDataQA;
delete [] binDataQB;
if (cleanUp==1)
	system( string( "rm "+string(argv[1]) ).c_str() );

return 0;}
