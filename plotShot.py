import pylab as plt #must install matplotlib
from sys import argv
from array import array

Nphi = 360

shotFile = open(argv[1],"r")

header = array('c')
header.fromfile(shotFile,1024)
print header
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
q = 0
while q < numQs*Nphi:
	row = binData[q:q+Nphi:1]
	I.append(row)
	q += Nphi

plt.figure(1)
plt.imshow(I,aspect="auto")
plt.show()

