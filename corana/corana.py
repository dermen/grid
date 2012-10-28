import os
from math import cos,sin,sqrt,pi
from sys import argv
import math
from array import array
from random import random,seed
from numpy import dot,identity,matrix,outer
import numpy as np
import re

def aveNo0(ar):
	ave = 0
	num = 0
	for i in ar:
		if i > 0:
			ave += i
			num += 1
	if num > 0:
		ave = ave / float(num)
		return ave
	else:
		return ave

def crossCor(ar1,ar2):
	NN = len(ar1)
	shotAve1 = aveNo0(ar1)
	shotAve2 = aveNo0(ar2)
	arC = array('f')
        phi = 0
        while phi < NN:
                i = 0
                CC = 0
		counts = 0
                while i < NN:
                        j = i+phi
                        if j >= NN:
                                j = j - NN
			CC += (ar1[i]-shotAve1)*(ar2[j]-shotAve2)/(shotAve1*shotAve2)
			#CC += (ar1[i]-shotAve1)*(ar2[j]-shotAve2)
                        i += 1
                arC.append( CC / NN )
                phi += 1
	return arC

cfgFile = open(argv[1],"r")

params = []
for line in cfgFile.readlines():
	if not re.search("^#",line):
	  if re.search("=",line):
	  	line= line.strip().split()
		key = line[0]
		val = line[2]
		params.append((key,val))

params = dict(params)

pathToCorana = params["pathToCorana"]
workDir    = params["workDir"]
numShots = params["numShots"]
samp = params["samp"]
anglesPerShot = params["anglesPerShot"]

Nphi =  int( params["Nphi"] )
computeAngAve = params["computeAngAve"]
pathToAngAve= params["pathToAngAve"]

shotDir = workDir + samp + "/shots/"
shotDir = shotDir + str(anglesPerShot) + "angles/"

shots = os.listdir(shotDir)

i = 0
while i < len(shots):
	shots[i] = shotDir + shots[i]
	i += 1

outDir = workDir + samp + "/cors/"
if not os.path.exists(outDir):
	os.makedirs(outDir)
outDir = outDir + str(anglesPerShot) + "angles/"
if not os.path.exists(outDir):
	os.makedirs(outDir)



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

shotFile.close()

i = 0
while i < len(shots):
	shotFile = open(shots[i],"r")
	shotFile.seek(1024)
	binData = array('f')
	binData.fromfile(shotFile,numQs*Nphi)
	j = 0
	corFileName = outDir + str(i) + "-cor.bin"
	print shots[i]
	corFile = open(corFileName,"w")
	header.tofile(corFile)
	while j < Nphi*numQs:
		row = binData[j:j+Nphi:1]
		CC = crossCor(row,row)
		CC.tofile(corFile)
		j += Nphi
	corFile.close()
	i += 1
	shotFile.close()
'''
cmd = [pathToCorana,Nphi,computeAngAve,pathToAngAve,numQs,outDir]
cmd = cmd + shots
cmd = " ".join(cmd)
os.system(cmd)'''
