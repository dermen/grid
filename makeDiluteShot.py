import os
import re
import math
from array import array
import random
from sys import argv

# will convert this file to c++ code

### **** ENTER USER PARAMS ****
totalAngles = 1000 # number of angles in each factor file
anglesPerShot = 20  #number of molecules/particles per shot
numShots = 1 # total number of simulated shots
workDir = "/Users/dermen/gridOut/"
samp = "pent"
shotQs = range(50,200,1) # range of q values to compute intensity 
#			              ^(0.02 Ang^1 units)
Nphi = 360 # number of angular bins per q in factor files
computeAngAve = True
### **** END **

sampDir = workDir + samp + "/"
outDir = sampDir + "shots/"
if not os.path.exists(outDir):
	os.makedirs(outDir)
outDir = outDir + str(anglesPerShot) + "angles/"
if not os.path.exists(outDir):
	os.makedirs(outDir)

factorDir = sampDir + "factors/" + str(totalAngles) + "angles/"

qFiles = []
factorFiles = os.listdir(factorDir)
for i in factorFiles:
	q = i.split(samp)[0]
	if shotQs.count( int(q) ) > 0:
		qFiles.append([int(q),factorDir +i])

qFiles = sorted(qFiles)
Qs = []
i = 0
while i < len(qFiles):
	q = qFiles[i][0]
	Qs.append(str(q))
	qFiles[i] = qFiles[i][1]
	i += 1
del factorFiles
del shotQs

### **** open output files **** ####
header = array('c')
header.fromstring("-".join(Qs))
while len(header) < 1024:
	header.append("&")
outFiles = []
i = 0
while i < numShots:
	outFileName = str(i) + ".bin"
	outFileName = outDir + outFileName
	outFile = open(outFileName,"w")
	header.tofile(outFile)
	outFiles.append(outFile)
	i += 1
### **** END *** 

#### *** PICK ORIENTATIONS FOR EACH SHOT *** 
shotIndex = 0
randomIndices = []
while shotIndex < numShots:
	i = 0
	while i < anglesPerShot:
		randomIndex = random.randrange(totalAngles)
		randomIndices.append(randomIndex)
		i += 1
	shotIndex += 1
#### ***** END **** 

qIndex = 0
while qIndex < len(Qs):
	binFileName = qFiles[qIndex]
	binFile = open(binFileName,"r")
	binDataA = array('f')
	binDataB = array('f')
	binDataC = array('f')
	# loading data into memory
	i = 0
	while i < totalAngles:
		binDataA.fromfile(binFile,Nphi)
		binDataB.fromfile(binFile,Nphi)
		j = 0
		while j < Nphi:
			valA = binDataA[i*Nphi + j]
			valB = binDataB[i*Nphi + j]
			val = valA*valA + valB*valB
			binDataC.append(val)
			j += 1
		i += 1

	del binDataA
	del binDataB

	shotIndex = 0
	while shotIndex < numShots:
		binData = array('f')
		randStart = shotIndex*anglesPerShot
		randStop = shotIndex*anglesPerShot + anglesPerShot
		randomInds = randomIndices[randStart:randStop:1]
		i = 0
		while i < Nphi:
			val = 0
			for j in randomInds:
				val += binDataC[j*Nphi + i]
			val = val / float(anglesPerShot)
			binData.append(val)
			i += 1
		binData.tofile(outFiles[shotIndex])
		shotIndex += 1
	qIndex += 1
	binFile.close()
	
i = 0
while i < numShots:
	outFiles[i].close()
	i += 1

if computeAngAve:
	os.system("python angAve.py "+outDir)
	
