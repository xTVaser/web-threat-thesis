# GADriver.py

Driving script used to run the genetic algorithm on the given input and produce output.  In real usage, GATest.py is used to perform automated testing.  The GA will run through all the combinations and output a file for each combination, for the number of iterations, etc.

Sample Usage:  
  
``
GADriver.py -p 100 -g 10 -m 0.5 -e 5 -i 1 -b 36 -f Length_Training_GA -o Test_GA
``

``-p``  Define the maximum population size per generation  

``-g``  Define the number of generations to compute  

``-m``  Percentage chance to mutate an allele  

``-e``  Top percentage of current population to carry over unchanged to the next generation   

``-i``  Repeat the genetic algorithm (i) times to generate more than the maximum population size at the end  

``-b``  Specify the number of multiple combinations of the same bitstring length excluding the decimal representation  

``-f``  File name containing requests and parsed bitstrings    

``-o``  output file name, the algorithm will be appended to the end automatically.
