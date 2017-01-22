import argparse
import sys
import os

trainingSize = 1000
testingSize = 5000

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--sqli", help="Path to file containing SQLi requests, line seperated")
parser.add_argument("-x", "--xss", help="Path to file containing XSS requests, line seperated")
parser.add_argument("-r", "--rfi", help="Path to file containing RFI requests, line seperated")
parser.add_argument("-n", "--nonthreats", help="Path to file containing Non-Threat requests, line seperated")

parser.add_argument("-sp", "--sqliPercentage", type=int, help="Proportion of SQLi requests in final test, up to 50")
parser.add_argument("-xp", "--xssPercentage", type=int, help="Proportion of XSS requests in final test, up to 50")
parser.add_argument("-rp", "--rfiPercentage", type=int, help="Proportion of RFI requests in final test, up to 50")
parser.add_argument("-np", "--nonthreatPercentage", type=int, help="Proportion of Non-Threat requests in final test, up to 10")

parser.add_argument("-t", "--training", action="store_true", help="Test will contain " + str(trainingSize) + " requests total")
parser.add_argument("-f", "--testing", action="store_true", help="Test will contain " + str(testingSize) + " requests total")

parser.add_argument("-o", "--outputFile", help="Name of the Output File")

args = parser.parse_args()


if (args.sqliPercentage + args.xssPercentage + args.rfiPercentage + args.nonthreatPercentage) != 100:
    sys.exit(-1)

os.chdir(os.getcwd())
print(os.getcwd())

choosenSize = trainingSize

if args.testing is True:
    choosenSize = testingSize

numSQL_Total = int(choosenSize * (args.sqliPercentage/100.0))
numXSS_Total = int(choosenSize * (args.xssPercentage/100.0))
numRFI_Total = int(choosenSize * (args.rfiPercentage/100.0))
numNT_Total = int(choosenSize * (args.nonthreatPercentage/100.0))


fileSQL = open(args.sqli).read().splitlines()
fileXSS = open(args.xss).read().splitlines()
fileRFI = open(args.rfi).read().splitlines()
fileNT = open(args.nonthreats).read().splitlines()

fileOutput = open(args.outputFile, "w+")

#The first 30% so 300 lines are going to be used for the training set of the genetic algorithm, so we need to put the same proportions into that one.
#Then the rest can be placed in the remainder of the file.
def outputtofile(file, counter, contents, offset, threatType):
    for i in range(int(counter)):
        file.write(str(threatType) + " " + contents[i+int(offset)] + "\n")

outputtofile(fileOutput, numSQL_Total * 0.30, fileSQL, 0, 1)
outputtofile(fileOutput, numXSS_Total * 0.30, fileXSS, 0, 2)
outputtofile(fileOutput, numRFI_Total * 0.30, fileRFI, 0, 3)
outputtofile(fileOutput, numNT_Total * 0.30, fileNT, 0, 0)

fileOutput.write("\n")

outputtofile(fileOutput, numSQL_Total * 0.70, fileSQL, numSQL_Total * 0.30, 1)
outputtofile(fileOutput, numXSS_Total * 0.70, fileXSS, numXSS_Total * 0.30, 2)
outputtofile(fileOutput, numRFI_Total * 0.70, fileRFI, numRFI_Total * 0.30, 3)
outputtofile(fileOutput, numNT_Total * 0.70, fileNT, numNT_Total * 0.30, 0)