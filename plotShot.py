import pylab as plt #must install matplotlib
from sys import argv
from array import array
import numpy as np

Nphi = 360

shotFile = open(argv[1],"r")

header = array('c')
header.fromfile(shotFile,1024)
header = header.tostring()
Qs = header.split("&")[0].split("-")
i = 0
while i < len(Qs):
	Qs[i] = int(Qs[i])
	i += 1

Qs = sorted(Qs)
numQs = len(Qs)

binData = array('f')
binData.fromfile(shotFile,Nphi*numQs)

shotFile.close()

I = []
qStart = 20
q = Nphi*qStart
aves = []
while q < numQs*Nphi:
	row = binData[q:q+Nphi:1]
	I.append(row)
	aves.append(np.average(row))
	q += Nphi

plotMin= np.average(I) - 0.85*np.std(I)
plotMax= np.average(I) + 1.85*np.std(I)

plt.figure(1)
plt.imshow(I,vmin=plotMin,vmax=plotMax,aspect="auto")

plt.figure(2)
plt.plot(range(len(aves)),aves)
plt.show()


