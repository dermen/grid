import os
import re
import math
from array import array
import random
from sys import argv

# will convert this file to c++ code


### **** ENTER USER PARAMS ****
workDir =  "/Users/dermen/gridOut/"
samp = "goldSmall"
sampDir = workDir + samp + "/"
factorDir = sampDir + "factors/"
anglesPerShot = 10  #number of molecules/particles per shot
numShots = 50 # total number of simulated shots
shotQs = range(50,200,1)
Nphi = 360
### **** END **** 

outDir = sampDir + "shots/"
if not os.path.exists(outDir):
	os.makedirs(outDir)
outDir = outDir + str(anglesPerShot) + "angles/"
if not os.path.exists(outDir):
	os.makedirs(outDir)

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
totalAngles = factorFiles[0].split("-")[1].split("angles")[0]
totalAngles = int(totalAngles)
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
	
i = 0
while i < numShots:
	outFiles[i].close()
	i += 1
