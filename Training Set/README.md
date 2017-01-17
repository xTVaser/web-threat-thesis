# TestGenerator.py

This small script takes in all of the files with the individual web attack types, and combines them to create a valid test file.  
  
For training it will divide the file into two segments, 30/70% of the file.  The first 30% is the initial set for the genetic algorithm but it will use the entire file.  For the support vector machine it doesnt matter as it will only pass through the file once.  

Training size = 1000 requests  
Testing size = 5000 requests  

Usage:  
  
``
TestGenerator.py -s SQL_Training -x XSS_Training -r RFI_Training -n NT_Training -sp 30 -xp 30 -rp 30 -np 10 -t -o TEST_Training
``

``-s``  file containing sql injection attacks, line seperated

``-x``  file containing xss attacks, line seperated 

``-r``  file containing rfi attacks, line seperated

``-n``   file containing non-attacks, line seperated 

``-sp``  percentage makeup of the file for sql attacks

``-xp`` percentage makeup of the file for xss attacks

``-rp``  percentage makeup of the file for remote file inclusion attacks

``-np``  percentage makeup of the file for non-attacks (false positive purposes)

``-t`` specify the test is for training

``-f`` specify the test is for testing

``-o`` output file path and name
