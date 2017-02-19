import argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from CommonLib.SVMRequest import getTrainingSet
from CommonLib.SVMRequest import getTestingSet

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--sqlNumber",
                    help="The number of SQL attacks to include in training")
parser.add_argument("-x", "--xssNumber",
                    help="The number of XSS attacks to include in training")
parser.add_argument("-r", "--rfiNumber",
                    help="The number of RFI attacks to include in training")
parser.add_argument("-n", "--ntNumber",
                    help="THe number of nonthreat attacks to include in training")

parser.add_argument("-t", "--type",
                    help="What attack type we are trying to identify")

parser.add_argument("-op", "--optimize", action="store_true",
                    help="Whether or not the svm should optimize gamma and C values using a GridSearch")

parser.add_argument("-f", "--fileDirectory",
                    help="Directory containing the 4 threat files for training")
parser.add_argument("-o", "--output",
                    help="Output file name")

args = parser.parse_args()

numSQL = int(args.sqlNumber)
numXSS = int(args.xssNumber)
numRFI = int(args.rfiNumber)
numNT = int(args.ntNumber)

type = int(args.type)

directory = args.fileDirectory

# Get all of the requests that we need from the files
# The number of each, the type that we are trying to identify.
# Will return a pair of two elements, the first being the requests and x,y positions, and the second being the targets 0 or 1
testing = getTestingSet(type, "Testing Data/")
training = getTrainingSet(numSQL, numXSS, numRFI, numNT, type, directory)


# Take the response and convert it into a numpy array to be used by the SVM



































print("Ye")