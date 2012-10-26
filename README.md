grid
====

simulates a correlated x-ray scattering experiment.

##1) use grid.py to create the scattering factors

###a) compile grid.cpp 
    g++ --fast-math -O3 grid.cpp -o GridFQ
###b) edit 
    grid/testFiles/*.cfg 
and save it somewhere else.
###c) make sure that numpy is installed. On ubuntu use
    apt-get install python-numpy etc. 
###d) run grid.py
    python grid.py path/to/*.cfg

##2) use makeDiluteShot.py to create simulated shots

###a) edit 
    grid/testFiles/shot.cfg 
###and save it somewhere else
###b) run makeDiluteShot.py
    python makeDiluteShot.py path/to/shot.cfg

##3) plot a shot in polar coordinates

###a) make sure that matplotlib is installed. e.g.
    apt-get install python-matplotlib
###b) plot a shot
    python plotShot.py workDir/samp/shots/Xangles/shot.bin

##4) more to come (and better instructions!)
