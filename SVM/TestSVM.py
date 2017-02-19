import os
import shutil
import sys
import time
from subprocess import DEVNULL, STDOUT, run

# Calling Syntax

# Setup Environment
print("Deleting Results Folder")
try:
    print("Deletion current disabled for testing reasons")
    # shutil.rmtree("Results/")
except:
    print("No Results Folder Found")

# os.mkdir("Results/")

def runTest(testName, folderStruct,
            population, generations, iterations, mutationRate, elitistPool, numBitstrings,
            input, output):

    print("")

    outputDir = "../Test Results/SVM/" + folderStruct + testName + "/"

    print("Running:\t" + testName + "\t\tWill be Stored In:\t" + outputDir)
    print("Arguments:\tPopulation: " + population +"\tGeneration: " + generations +
          "\tIterations: " + iterations + "\tMutation Rate: " + mutationRate +
          "\tElitist Pool: " + elitistPool + "\tNumber of Bitstrings: " + numBitstrings)

    timeStart = time.time()

    cmd = ("python3 GADriver.py -p" + population + " -g " + generations +
           " -m " + mutationRate + " -e " + elitistPool + " -i " + iterations +
           " -b " + numBitstrings + " -f " + input + " -o " + output)

    sys.stdout.write("...")
    sys.stdout.flush()
    run(cmd.split(), stdout=DEVNULL, stderr=STDOUT)

    resultFiles = os.listdir("Results/")

    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    testResults = []

    for file in resultFiles:

        shutil.move("Results/" + file, outputDir + file)

    timeEnd = time.strftime("%M:%S", time.localtime(time.time() - timeStart))
    sys.stdout.write("Finished in " + str(timeEnd) + "\n")

    return testResults

def moveTestingResults(directory, results):

    print("stub")

# Defined Tests Below
# Fair Comparisons using the same ratios as the genetic algorithm testing (30/30/30/10)



