# Commandline Arguments
import argparse
from CommonLib import convertRequests
from GeneticAlgorithm import genAlgorithm

parser = argparse.ArgumentParser()

parser.add_argument("-p", "--population", help="Define the maximum population size per generation")
parser.add_argument("-g", "--generation", help="Define the number of generations to compute")
parser.add_argument("-m", "--mutationRate", help="Percentage chance to mutate a gene (0.1 - 1.0)")
parser.add_argument("-e", "--elitistPool", help="Top percentage of current population to carry over unchanged to the next generation")
parser.add_argument("-i", "--iterations", help="Repeat the genetic algorithm (i) times to generate more than the maximum population size at the end")

# If there are multiple combinations of the same bitstring, we need to compare on the respective bitstring sizes, not mixing and matching
# So the GA will run through all the combinations and output a file for each combination, for the number of iterations, etc.
parser.add_argument("-b", "--bitstrings", help="Specify the number of multiple combinations of the same bitstring length excluding the decimal representation")

parser.add_argument("-f", "--file", help="File name containing requests and parsed bitstrings")
parser.add_argument("-o", "--output", help="Output file name")

args = parser.parse_args()

# First read in all of the data from the parsed test files into some form of object structure
# These objects will contain the header information for the requests (what the request was and what type it truly is)
# They will also contain all of the bitstrings that the request may be interpreted as (sql/xss/rfi)
initialPop = convertRequests(args.file)

# Setup initial population
tranSet = initialPop[0]
testSet = initialPop[1]

sqlResults = []
xssResults = []
rfiResults = []

# Initialize Results for each bitstring length
# CHANGE THIS to add the length information
for x in range(int(args.bitstrings)):
    sqlResults.append([])
    xssResults.append([])
    rfiResults.append([])

# Call genetic algorithm function for each attack type
for n in range(int(args.iterations)):
    tempSQL = genAlgorithm(tranSet.copy(), testSet.copy(),
                           int(args.population), int(args.generation), float(args.mutationRate), int(args.elitistPool),
                           1, int(args.bitstrings))
    tempXSS = genAlgorithm(tranSet.copy(), testSet.copy(),
                           int(args.population), int(args.generation), float(args.mutationRate), int(args.elitistPool),
                           2, int(args.bitstrings))
    tempRFI = genAlgorithm(tranSet.copy(), testSet.copy(),
                           int(args.population), int(args.generation), float(args.mutationRate), int(args.elitistPool),
                           3, int(args.bitstrings))

    # Add each of the results for each length to the respective list in the results.
    for i in range(int(args.bitstrings))-1:

        sqlResults[i] += tempSQL[i]
        xssResults[i] += tempXSS[i]
        rfiResults[i] += tempRFI[i]


# Output to file
for n in range(args.bitstrings):

    sqlOutput = None
    xssOutput = None
    rfiOutput = None

    if args.bitstrings > 1:
        #Add the bitstring lengths to the filename
        sqlOutput = open("RESULTS_SQL_" + sqlResults[n].pop(0) + "_" + args.output, "w+")
        xssOutput = open("RESULTS_XSS_" + xssResults[n].pop(0) + "_" + args.output, "w+")
        rfiOutput = open("RESULTS_RFI_" + rfiResults[n].pop(0) + "_" + args.output, "w+")

    else:
        sqlOutput = open("RESULTS_SQL_" + args.output, "w+")
        xssOutput = open("RESULTS_XSS_" + args.output, "w+")
        rfiOutput = open("RESULTS_RFI_" + args.output, "w+")

    for line in sqlResults[n]:
        sqlOutput.write(line + "\n")

    for line in xssResults[n]:
        xssOutput.write(line + "\n")

    for line in rfiResults[n]:
        rfiOutput.write(line + "\n")