grid
====

simulates a correlated x-ray scattering experiment

1) use grid.py to create the scattering factors

  a) compile grid.cpp 
	g++ --fast-math -O3 grid.cpp -o GridFQ
  b) edit testFiles/*.cfg and save it somewhere else
  c) run grid.py
	python grid.py path/to/*.cfg

2) use makeDiluteShot.py to create simulated shots

3) more to come (and better instructions!)
