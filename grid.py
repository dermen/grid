import os
from math import cos,sin,sqrt,pi
from sys import argv
import math
from array import array
from random import random,seed
from numpy import dot,identity,matrix,outer
import numpy as np
import re

PathToGrid = "/Users/dermen/gridFiles/polar/grid/GridFQ"

workDir = "/Users/dermen/gridOut/"

coorInputFileName = "pent.coor" #should be in working directory
'''

*.coor should be an N-line txt file in this format:
x1 y1 z1 AtomID1
x2 y2 z2 AtomID2
...
...
xN yN zN AtomIDN

'''

#Q values to consider (in units of 0.02 Ang^-1)
Qs = range(0,250,1)
# 1.00 Ang^-1 to 3.98 Ang^-1 in steps of 0.02 Ang^-1

#Qs = [124,252] # 2.48 Ang^-1 and 5.04 Ang^-1
numQs = len(Qs)

# number of sample points along the diffraction ring
Nphi = "360" # 1 degree angular resolution

numAngles = 1000 #orientations
# ^ this will be the number of random orientations at which 
#   the scattering factors will be computed

# enter 1 to delete randomly generated atomic coors
# after completion; 0 if you want to keep them
cleanUp = "1"

if re.search("/",coorInputFileName):
	samp = coorInputFileName.split("/")[-1].split(".coor")[0]
#	^ samp = "pent" in this case
else:
	samp = coorInputFileName.split(".coor")[0]

# algorithm for generating a uniform random orientation of a sphere
def RandomRotation():
#	3 random numbers
	x1 = random()*2*pi
	seed()
	x2 = random()*2*pi
	seed()
	x3 = random()
	seed()
	
#	matrix for rotation about z-axis
	Rz1 = [cos(x1),sin(x1),0]
	Rz2 = [-sin(x1),cos(x1),0]
	Rz3 = [0,0,1]
	R = matrix([Rz1,Rz2,Rz3])

#	matrix for rotating the pole
	v = [cos(x2)*sqrt(x3),sin(x2)*sqrt(x3),sqrt(1-x3)]
	v = np.array(v)
	I = identity(3)
	H = I - 2*outer(v,v)
	M = -H*R
	return M

#generate a sub directory for output
if workDir[-1] != "/":
	workDir = workDir + "/"
outDir = workDir + samp + "/"
if not os.path.exists(outDir):
	os.makedirs(outDir)
outDir = outDir + "factors/"
if not os.path.exists(outDir):
	os.makedirs(outDir)
outDir = outDir + str(numAngles)+"angles/"
if not os.path.exists(outDir):
	os.makedirs(outDir)

# read in the atomic info (coors and ID)
moleculeStructure = []
for i in open(workDir + coorInputFileName,'r').readlines():
	i = i.strip().split()
	x = float(i[0])
	y = float(i[1])
	z = float(i[2])
	A = float(i[3]) #atom ID
	moleculeStructure.append(x)
	moleculeStructure.append(y)
	moleculeStructure.append(z)
	moleculeStructure.append(A)

# number of coordinates per shot (passed as a parameter later)
coorPerShot = len(moleculeStructure)

numProcs = 1
shotsPerProc = numAngles / numProcs

wavelen = 0.7293 # keV
qRes = 0.02 # Ang^-1
qStart = 0.01 # Ang^-1

procIndex = 0
while procIndex < numProcs:
	coorFileName = outDir+"coordinates-"+str(procIndex)+".bin"
	coorFile = open(coorFileName,'w')
	n = 0
	while n < shotsPerProc:
		coordinates = array('f') # array for storing molecular coordinates
		rotMat = RandomRotation()
		row00 = float(rotMat[0,0])
		row01 = float(rotMat[0,1])
		row02 = float(rotMat[0,2])
		row10 = float(rotMat[1,0])
		row11 = float(rotMat[1,1])
		row12 = float(rotMat[1,2])
		row20 = float(rotMat[2,0])
		row21 = float(rotMat[2,1])
		row22 = float(rotMat[2,2])
#		generate the rotated molecular coordinates
		i = 0
		while i < len(moleculeStructure):
#			original coordinates of each atom in molecule
			x = moleculeStructure[i]
			y = moleculeStructure[i+1]
			z = moleculeStructure[i+2]
			A = moleculeStructure[i+3]
#			apply the randomRotation
			newX = row00*x + row01*y + row02*z
			newY = row10*x + row11*y + row12*z
			newZ = row20*x + row21*y + row22*z
#			save coordinates
			coordinates.append(newX)
			coordinates.append(newY)
			coordinates.append(newZ)
			coordinates.append(A)
			i += 4
#		save coordinate file
		coordinates.tofile(coorFile)
		n += 1
	coorFile.close()

#	calculate rings of diffraction at listed q values
	qArray = []
	outFileNames = []
	for q in Qs:
		qA = q*qRes + qStart
		theta = math.asin( qA*wavelen / (4*math.pi) )
		qArray.append( str( theta ) )
		qArray.append( str( qA    ) )
		qArray.append( str( q     ) )
		outFileName = str(q)+samp+"-"+str(procIndex)+".bin"
		outFileName = outDir + outFileName
		outFileNames.append(outFileName)
	numOutFileNames = str( len(Qs) )
	cmd = [PathToGrid,coorFileName,str(coorPerShot),str(shotsPerProc),Nphi,cleanUp,numOutFileNames]
	cmd+= outFileNames
	cmd+= qArray
	cmd = " ".join(cmd)
	print cmd
	os.system(cmd)
	procIndex += 1
