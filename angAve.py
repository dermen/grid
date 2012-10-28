from sys import argv
from array import array
import os
import re

Nphi = 360

shotDir =  argv[1] 
if shotDir[-1] != "/":
	shotDir = shotDir + "/"

shots = []
for i in os.listdir(shotDir):
	if re.search(".bin",i):
		shots.append(shotDir + i) 

# get header of first shot (same on all shots)
shotFile = open(shots[0],"r")
header = array('c')
header.fromfile(shotFile,1024)
h = header.tostring()
Qs = h.split("&")[0].split("-")
i = 0
while i < len(Qs):
	Qs[i] = int(Qs[i])
	i += 1
numQs = len(Qs)

sumData = array('f')
sumData.fromfile(shotFile,Nphi*numQs)

shotFile.close()

i = 1
while i < len(shots):
	shotFile=open(shots[i],"r")
	shotFile.seek(1024)

	binData = array('f')
	binData.fromfile(shotFile,Nphi*numQs)

	j = 0
	while j < Nphi*numQs:
		sumData[j] += binData[j]
		j += 1

	shotFile.close()
	i += 1

outFileName = shotDir + "angAve.bin"
outFile = open(outFileName,"w")
header.tofile(outFile)
sumData.tofile(outFile)
outFile.close()

