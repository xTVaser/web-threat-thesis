import argparse
import sys
import os

from threats.rfi import rfiBitstring
#from threats.sql import sqlBitstring
#from threats.xss import xssBitstring

os.chdir(os.getcwd())

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", help="Path to file containing threat information and requests")

parser.add_argument("-ga", "--geneticAlgorithm", action="store_true", help="The produced bitstrings will be for the Genetic Algorithm approach")
parser.add_argument("-svm", "--supportVectorMachine", action="store_true", help="The produced bitstrings will be for the SVM approach")

parser.add_argument("-b", "--bitstring", help="Specify the max length of each of the 4 bitstring segments, each of a max of 8. ex 4444 or 4141")
parser.add_argument("-d", "--decimal", action="store_true", help="The first bitstring will be in normal integer format in addition to the other binary bitstrings")
parser.add_argument("-p", "--permute", help="Will permute all combinations of the bitstring up to the specified max length. Gen.Algo Only")

parser.add_argument("-o", "--output", help="Specify the output filename")

args = parser.parse_args()

# Figure out if it is for GA or SVM
isSVM = False
if args.geneticAlgorithm is False and args.supportVectorMachine is True:
    isSVM = True

# Change the bitstring length argument into an int list.
bitstringLengths = args.bitstring.split("")
for length in bitstringLengths:
    length = int(length)

#First step is to get all of the requests from the file into some kind of list structure

inputFile = open(args.file)

requests = []

for line in inputFile:
    if line == "\n":
        continue
    else:
        contents = line.split(" ")
        requests.append((contents[0], contents[1]))

parseOutput = []

# Start constructing the output each request will be as follows:
# <threat type (0-3)> <original request>
# 10.124.4.2 1010.111.1.111 ....           - SQL LINE
# Same as above but XSS
# Same as above but RFI

# Method will permute all bitstrings and return a string with all combinations.
def permuteBitstrings(decBitstring, bitstringLength):
    return "decbitstring bitstring2 bitstring3...."

# Call each method to get the bitstrings in normal decimal form, then we can turn them into binary here.
for request in requests:

    parseOutput.append(request[0] + " " + request[1])

    # Pass it to each method for it to return a list of the values for each segment.
    sql = sqlBitstring(request[1], bitstringLengths, isSVM)
    xss = xssBitstring(request[1], bitstringLengths, isSVM)
    rfi = rfiBitstring(request[1], bitstringLengths, isSVM)

    # Here I would print out all permuted bitstrings if that flag was set but for now, just print out one

# Create output file
outputFile = None
if isSVM is True:
    outputFile = open(args.output+"_SVM", "w+")
else:
    outputFile = open(args.output+"_GA", "w+")

#Then print out all the lines in the file.
for line in parseOutput:
    outputFile.write(line + "\n")