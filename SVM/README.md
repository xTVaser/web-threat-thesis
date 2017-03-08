# SVM.py

Script that builds an SVM for every detection each of the three attack types, and each of the three kernels given training input and determines results from testing input. In real usage, TestSVM.py would be used to call this program to allow for automated testing of a large amount of results. 

Sample Usage:  
  
``
SVM.py -s 1000 -x 1000 -r 1000 -n 350 -f Training/New/ -o 75_25
``

``-s``  The number of SQL attacks to include in training  

``-x``  The number of XSS attacks to include in training   

``-r``  The number of RFI attacks to include in training  

``-n``  The number of nonthreat attacks to include in training  

``-f``  Directory containing the 4 threat files for training 

``-o``  Output file name  
