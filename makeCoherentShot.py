import os
import math
from array import array
import random
from sys import argv
import pylab as plt

def collisionDetection(arX,arY,arZ,x,y,z,l):
        collisionX = False
        collisionY = False
        collisionZ = False
        for i in arX:
                if x > i-l and x < i+l:
                        collisionX = True
        for i in arY:
                if y > i-l and y < i+l:
                        collisionY = True
        for i in arZ:
                if z > i-l and z < i+l:
                        collisionZ = True
        if collisionX and collisionY and collisionZ:
                return True
        else:
                return False

Nphi = 360
phiRange = range(Nphi)

numAngles = 100000

binFile = open(argv[1],"r")
binDataA = array('f')
binDataB = array('f')

i = 0
while i < numAngles:
	binDataA.fromfile(binFile,Nphi)
	binDataB.fromfile(binFile,Nphi)
	i += 1

#parameters for translation of molecule
q = 133
qRes = 0.02
qStart = 0.01
wavelen = 0.7293
qA = qRes*q + qStart
theta = math.asin(qA*wavelen / (math.pi*4 ) )
qZ = qA*math.sin(theta)
cosTheta = math.cos(theta)
dphi = float(Nphi / (2* math.pi) )
qXs = [qA * cosTheta * math.cos(i * dphi) for i in range(Nphi)]
qYs = [qA * cosTheta * math.sin(i * dphi) for i in range(Nphi)]

numShots = 20
anglesPerShot = 2000000

#collision detction parameters
ls = 71.7
box = anglesPerShot*2000*ls

dir = argv[2]
if dir[-1] != "/":
	dir = dir + "/"
outDirName = str(numShots) + "shots-" + str(anglesPerShot)+"angles-coherent/"
outDir = dir + outDirName
if not os.path.exists(outDir):
	os.makedirs(outDir)

shotIndex = 2
while shotIndex < numShots+2:
	binData = array('f')
	randomIndices = []
#       initialize arrays with pseudo coordinate (for collision detection)
	rangeX = [99999999]
        rangeY = [99999999]
        rangeZ = [99999999]
	i = 0
	while i < anglesPerShot:
		randomIndex = random.randrange(numAngles)
		randomIndices.append(randomIndex)
#               generate translation vector
                while 1:
#                       generate random position
                        shiftX = (random.random() - 0.5)*box
                        shiftY = (random.random() - 0.5)*box
                        shiftZ = (random.random() - 0.5)*box
#                       check for collision
#                        -the factor 2.0 scales inversely with the density 
#                         of the molecules
                        if not collisionDetection(rangeX,rangeY,rangeZ,\
                        shiftX,shiftY,shiftZ,2.0*ls):
                                break
#               save position
                rangeX.append(shiftX)
                rangeY.append(shiftY)
                rangeZ.append(shiftZ)
		i += 1
	rangeX.pop(0)
	rangeY.pop(0)
	rangeZ.pop(0)
	i = 0
	while i < Nphi:
		valR = 0
		valI = 0
		jj = 0
		for j in randomIndices:
			FA = binDataA[j*Nphi + i]
			FB = binDataB[j*Nphi + i]
			phase = qXs[i]*rangeX[jj]
			phase+= qYs[i]*rangeY[jj]
			phase+= qZ*rangeZ[jj]
			c = math.cos(phase)
			s = math.sin(phase)
			valR += c*FA - s*FB
			valI += c*FB + s*FA
			jj += 1
		val = valR*valR + valI*valI
		binData.append(val)
		i += 1
	outFileName = outDir + "133-"+str(shotIndex) + ".bin"
	outFile = open(outFileName,"w")
	binData.tofile(outFile)
	print numShots - shotIndex
	shotIndex += 1

plt.figure(1)
plt.plot(phiRange,binData)
plt.show()

