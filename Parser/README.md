# RequestParser.py

This small script takes in a file that holds all of the requests for the test and will extract the various metrics from each. For example: number of keywords, number of urls, attack type, etc.  

Usage:  
  
``
RequestParser.py -f pathto/input.txt -ga -b 4444 -p -d -o output  
``

``-f``  file input with requests, line seperated with each line being in the syntax <attack type as integer> <request>  

``-ga``  parse the bitstrings for the use in a genetic algorithm.  

``-svm``  parse the bitstrings for the use in a supper vector machine algorithm.  

``-b``   specify the max length of each of the 4 segments in the bitstring (genetic algorithm only) Each segment can be a max length of 8.  

``-d``  the first bitstring will be printed out as a decimal number instead of binary.  

``-p``  permute the bitstrings to get all possible combinations up to the max length.  

``-o``  output file name, the algorithm will be appended to the end automatically.  
