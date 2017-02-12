import os
import shutil
import sys
import time
from subprocess import DEVNULL, STDOUT, run
from Lib.CommonLib import getLengthDictionary

# Calling Syntax
# --population <Integer> Max population per generation
# --generation <Integer> Number of generations per iteration
# --iterations <Integer> Number of iterations of the algorithm to combine
# --mutationRate <Float (0 - 1.0 are reasonable)> Chance of flipping a bit after generating offspring
# --elitistPool <Integer> Percentage of top performing bitstrings to preserve

# --bitstrings <Integer> Used for Length training, number of bitstrings per request.

# --file <String> Name of the test file input
# --output <String> Name of output file path.

normalTest = "Training_GA"
lengthTest = "Length_Training_GA"

# Setup Environment
print("Deleting Results Folder")
try:
    print("Deletion current disabled for testing reasons")
    # shutil.rmtree("Results/")
except:
    print("No Results Folder Found")

# os.mkdir("Results/")

def getLengthInfo(filename):

    if "LEN" in filename:
        return filename.split("_")[3]
    return None

def runTest(testName, folderStruct,
            population, generations, iterations, mutationRate, elitistPool, numBitstrings,
            input, output):

    print("")

    outputDir = "../Test Results/Genetic Algorithm/" + folderStruct + testName + "/"

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

        if file.endswith(".res"):

            type = 3

            if "SQL" in file:
                type = 1
            elif "XSS" in file:
                type = 2

            testResults.append([type, testName] + getTestingResults(open("Results/" + file).readlines(), type, getLengthInfo(file)))

            shutil.move("Results/" + file, outputDir + file)

    timeEnd = time.strftime("%M:%S", time.localtime(time.time() - timeStart))
    sys.stdout.write("Finished in " + str(timeEnd) + "\n")

    return testResults

print("Generating Test Dictionaries")
lengthDictionary = getLengthDictionary(True)
normalDictionary = getLengthDictionary(False)
print("Test Dictionaries Generated\n")

def getTestingResults(generatedBitstrings, type, lengthInfo):

    signatureSet = []

    for line in generatedBitstrings:

        signatureSet.append(line.replace("\n", "").split())

    testingSet = None
    key = ""

    if type is 1:
        key = "_SQL"
    elif type is 2:
        key = "_XSS"
    else:
        key = "_RFI"

    if lengthInfo is None:
        testingSet = normalDictionary["6163" + key]
    else:
        testingSet = lengthDictionary[lengthInfo + key]

    successfulDetections = 0
    successfulDetection = False
    falsePositives = 0
    falsePositiveFlag = False
    wrongTypeDetection = 0
    wrongDetection = False

    for potentialAttack in testingSet:

        for signature in signatureSet:

            if potentialAttack[0] == signature and int(potentialAttack[1]) == type:

                successfulDetections += 1
                successfulDetection = True
                break

            elif potentialAttack[0] == signature and int(potentialAttack[1]) == 0:

                falsePositives += 1
                falsePositiveFlag = True
                break

            elif potentialAttack[0] == signature and int(potentialAttack[1]) != type:

                wrongDetection = True

        # If we wrong detect, we give it a chance to either false positive or find the proper bitstring b
        # but if it still was unable, then it was a false detection
        if wrongDetection is True and falsePositiveFlag is False and successfulDetection is False:
            wrongTypeDetection += 1

        successfulDetection = False
        falsePositiveFlag = False
        wrongDetection = False

    output = [str(successfulDetections), str(falsePositives), str(wrongTypeDetection)]

    return output

def printTestingResults(directory, results):

    sqlResults = open(directory + "Results_SQL.dat", "w+")
    xssResults = open(directory + "Results_XSS.dat", "w+")
    rfiResults = open(directory + "Results_RFI.dat", "w+")

    for test in results:
        for result in test:

            currentFile = None
            if result[0] is 1:
                currentFile = sqlResults
            elif result[0] is 2:
                currentFile = xssResults
            else:
                currentFile = rfiResults

            for i in range(len(result)-1):

                if i+1 is 2:
                    currentFile.write(str(int(result[i + 1]) / 1500.0 * 100.0) + "\t")

                elif i+1 is 3:
                    currentFile.write(str(int(result[i + 1]) / 500.0 * 100.0) + "\t")

                elif i+1 is 4:
                    currentFile.write(str(int(result[i + 1]) / 3000.0 * 100.0))

                else:
                    currentFile.write(result[i + 1] + "\t")

            currentFile.write("\n")

    sqlResults.close()
    xssResults.close()
    rfiResults.close()


print("(1) - Population Size Test")
print("(2) - Generation Test")
print("(3) - Mutation Rate Test")
print("(4) - Elitist Pool Test")
print("(5) - Iteration Test")
print("(6) - Bitstring Length Test")
testSet = int(input("Choose Test: "))

# Define Tests Below

# Determine Best Population Size ==========
# More individuals being generated increases the chances of generating better bitstrings.
if testSet is 1:

    testResults = []

    # 300 - Maximum number of each attack type in training set
    testResults.append(runTest("300", "Determine Best Settings/Population Size/",
                               "300", "100", "1", "0.5", "5", "1", "Training_GA", "300_Pop"))

    # 600 - Doubled previous
    testResults.append(runTest("600", "Determine Best Settings/Population Size/",
                               "600", "100", "1", "0.5", "5", "1", "Training_GA", "600_Pop"))

    # 1200 - Now above the size of the training set
    testResults.append(runTest("1200", "Determine Best Settings/Population Size/",
                               "1200", "100", "1", "0.5", "5", "1", "Training_GA", "1200_Pop"))

    # 2500 - Maximum
    testResults.append(runTest("2500", "Determine Best Settings/Population Size/",
                               "2500", "100", "1", "0.5", "5", "1", "Training_GA", "2500_Pop"))

    # 5000 - Double the Maximum
    testResults.append(runTest("5000", "Determine Best Settings/Population Size/",
                               "5000", "100", "1", "0.5", "5", "1", "Training_GA", "5000_Pop"))

    printTestingResults("../Test Results/Genetic Algorithm/Determine Best Settings/Population Size/", testResults)


# Determine Best Generation Setting =======
elif testSet is 2:

    testResults = []

    # 1
    testResults.append(runTest("1", "Determine Best Settings/Generations/",
                               "1250", "1", "1", "0.5", "5", "1", "Training_GA", "1_Gen"))

    # 50
    testResults.append(runTest("50", "Determine Best Settings/Generations/",
                               "1250", "50", "1", "0.5", "5", "1", "Training_GA", "50_Gen"))

    # 100
    testResults.append(runTest("100", "Determine Best Settings/Generations/",
                               "1250", "100", "1", "0.5", "5", "1", "Training_GA", "100_Gen"))

    # 500
    testResults.append(runTest("500", "Determine Best Settings/Generations/",
                               "1250", "500", "1", "0.5", "5", "1", "Training_GA", "500_Gen"))

    # 1000
    testResults.append(runTest("1000", "Determine Best Settings/Generations/",
                               "1250", "1000", "1", "0.5", "5", "1", "Training_GA", "1000_Gen"))

    printTestingResults("../Test Results/Genetic Algorithm/Determine Best Settings/Generations/", testResults)


# Determine Best Mutation Rate ============
elif testSet is 3:

    testResults = []

    # 0
    testResults.append(runTest("0.0", "Determine Best Settings/Mutation Rate/",
                               "1250", "100", "1", "0.0", "5", "1", "Training_GA", "0_0_Mut"))

    # 0.10
    testResults.append(runTest("0.10", "Determine Best Settings/Mutation Rate/",
                               "1250", "100", "1", "0.1", "5", "1", "Training_GA", "0_1_Mut"))

    # 0.25
    testResults.append(runTest("0.25", "Determine Best Settings/Mutation Rate/",
                               "1250", "100", "1", "0.25", "5", "1", "Training_GA", "0_25_Mut"))

    # 0.5
    testResults.append(runTest("0.5", "Determine Best Settings/Mutation Rate/",
                               "1250", "100", "1", "0.5", "5", "1", "Training_GA", "0_5_Mut"))

    # 1.0
    testResults.append(runTest("1.0", "Determine Best Settings/Mutation Rate/",
                               "1250", "100", "1", "1.0", "5", "1", "Training_GA", "1_0_Mut"))

    printTestingResults("../Test Results/Genetic Algorithm/Determine Best Settings/Mutation Rate/", testResults)


# Determine Best Elitist Pool =============
elif testSet is 4:

    testResults = []

    # 0
    testResults.append(runTest("0", "Determine Best Settings/Elitist Pool/",
                               "1250", "100", "1", "0.5", "0", "1", "Training_GA", "0_Elite"))

    # 2
    testResults.append(runTest("2", "Determine Best Settings/Elitist Pool/",
                               "1250", "100", "1", "0.5", "2", "1", "Training_GA", "2_Elite"))

    # 5
    testResults.append(runTest("5", "Determine Best Settings/Elitist Pool/",
                               "1250", "100", "1", "0.5", "5", "1", "Training_GA", "5_Elite"))

    # 10
    testResults.append(runTest("10", "Determine Best Settings/Elitist Pool/",
                               "1250", "100", "1", "0.5", "10", "1", "Training_GA", "10_Elite"))

    # 25
    testResults.append(runTest("25", "Determine Best Settings/Elitist Pool/",
                               "1250", "100", "1", "0.5", "25", "1", "Training_GA", "25_Elite"))

    printTestingResults("../Test Results/Genetic Algorithm/Determine Best Settings/Elitist Pool/", testResults)


# Iteration Comparison ====================
elif testSet is 5:

    testResults = []

    # 1 - Only one test
    testResults.append(runTest("1", "Multiple Iterations/",
                               "1250", "100", "1", "0.5", "5", "1", "Training_GA", "1_Iter"))

    # 2
    testResults.append(runTest("2", "Multiple Iterations/",
                               "1250", "100", "2", "0.5", "5", "1", "Training_GA", "2_Iter"))

    # 5
    testResults.append(runTest("5", "Multiple Iterations/",
                               "1250", "100", "5", "0.5", "5", "1", "Training_GA", "5_Iter"))

    # 10
    testResults.append(runTest("10", "Multiple Iterations/",
                               "1250", "100", "10", "0.5", "5", "1", "Training_GA", "10_Iter"))

    # 20 - 20 Tests combined
    testResults.append(runTest("20", "Multiple Iterations/",
                               "1250", "100", "20", "0.5", "5", "1", "Training_GA", "20_Iter"))

    printTestingResults("../Test Results/Genetic Algorithm/Multiple Iterations/", testResults)


# Bitstring Length Comparison =============
elif testSet is 6:

    testResults = []

    # One Test With the Best Settings
    testResults.append(runTest("BSLen", "Bitstring Length/",
                               "1250", "100", "1", "0.5", "5", "36", "Length_Training_GA", "BS_Len"))

    printTestingResults("../Test Results/Genetic Algorithm/Bitstring Length/", testResults)