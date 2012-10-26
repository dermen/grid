import os
import math
from array import array
import random
from sys import argv
import pylab as plt
import datetime

totalAngles = 100000
numShots = 50
anglesPerShot = 1000000
Q = "133"
samp = "goldMed"

dir = samp + "/"
if dir[-1] != "/":
	dir = dir + "/"

outDir = dir + Q + "-"+str(numShots)+"shots-"+str(anglesPerShot)+"angles-dilute/"

if os.path.exists(outDir):
	print "directory ",outDir,"already exists!"
	dt = datetime.datetime.today()
	dt = (str(dt)).split('.')[0]
	dt = "_".join(dt.split())
	outDir = outDir.split("dilute/")[0] + "-dilute" + dt + "/"
	print "creating directory ",outDir
	os.makedirs(outDir)
else:
	print "creating directory ",outDir
	os.makedirs(outDir)

Nphi = 360
phiRange = range(Nphi)

binFileName = argv[1]
binFile = open(binFileName,"r")
binDataA = array('f')
binDataB = array('f')
binDataC = array('f')

i = 0
print "loading data into memory..."
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
	#print totalAngles - i
	i += 1

del binDataA
del binDataB

shotIndex = 0
while shotIndex < numShots:
	binData = array('f')
	randomIndices = []
	i = 0
	while i < anglesPerShot:
		randomIndex = random.randrange(totalAngles)
		randomIndices.append(randomIndex)
		print anglesPerShot - i
		i += 1
	i = 0
	while i < Nphi:
		val = 0
		for j in randomIndices:
			val += binDataC[j*Nphi + i]
		val = val / float(anglesPerShot)
		binData.append(val)
		print Nphi - i
		i += 1
	outFileName = outDir + Q+"-"+str(shotIndex) + ".bin"
	outFile = open(outFileName,"w")
	binData.tofile(outFile)
	#print numShots - shotIndex
	shotIndex += 1

plt.figure(1)
plt.plot(phiRange,binData)
plt.show()
