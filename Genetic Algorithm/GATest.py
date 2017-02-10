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
log = open("Results/OVERALL_TEST_RESULTS", "w+")

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

    for file in resultFiles:

        if file.endswith(".res"):

            log.write(testName + "\t\tWill be Stored In:\t" + outputDir + "\n")
            log.write("Population: " + population +"\tGeneration: "+ generations +
                      "\tIterations: " + iterations + "\tMutation Rate: " + mutationRate +
                      "\tElitist Pool: " + elitistPool + "\tNumber of Bitstrings: " + numBitstrings + "\n"
                      "-------------------------\n")

            testResults = None
            type = 3

            if "SQL" in file:
                type = 1
            elif "XSS" in file:
                type = 2

            outputFile = open(outputDir + file + ".stats", "w+")
            testResults = getTestingResults(open("Results/" + file).readlines(), type, getLengthInfo(file))

            for result in testResults:

                log.write(result + "\n")
                outputFile.write(result + "\n")

            log.write("\n")
            outputFile.close()

            shutil.move("Results/" + file, outputDir + file)

    timeEnd = time.strftime("%M:%S", time.localtime(time.time() - timeStart))
    log.write("Time Taken: " + str(timeEnd) + "\n\n")
    sys.stdout.write("Finished in " + str(timeEnd) + "\n")

    return

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

    # 300 - Maximum number of each attack type in training set
    runTest("300Pop", "Determine Best Settings/Population Size/",
            "300", "100", "1", "0.5", "5", "1", "Training_GA", "300_Pop")

    # 600 - Doubled previous
    runTest("600Pop", "Determine Best Settings/Population Size/",
            "600", "100", "1", "0.5", "5", "1", "Training_GA", "600_Pop")

    # 1200 - Now above the size of the training set
    runTest("1200Pop", "Determine Best Settings/Population Size/",
            "1200", "100", "1", "0.5", "5", "1", "Training_GA", "1200_Pop")

    # 2500 - Maximum
    runTest("2500Pop", "Determine Best Settings/Population Size/",
            "2500", "100", "1", "0.5", "5", "1", "Training_GA", "2500_Pop")

    # 5000 - Double the Maximum
    runTest("5000Pop", "Determine Best Settings/Population Size/",
            "5000", "100", "1", "0.5", "5", "1", "Training_GA", "5000_Pop")


# Determine Best Generation Setting =======
elif testSet is 2:

    # 1
    runTest("1Gen", "Determine Best Settings/Generations/",
            "1250", "1", "1", "0.5", "5", "1", "Training_GA", "1_Gen")

    # 50
    runTest("50Gen", "Determine Best Settings/Generations/",
            "1250", "50", "1", "0.5", "5", "1", "Training_GA", "50_Gen")

    # 100
    runTest("100Gen", "Determine Best Settings/Generations/",
            "1250", "100", "1", "0.5", "5", "1", "Training_GA", "100_Gen")

    # 500
    runTest("500Gen", "Determine Best Settings/Generations/",
            "1250", "500", "1", "0.5", "5", "1", "Training_GA", "500_Gen")

    # 1000
    runTest("1000Gen", "Determine Best Settings/Generations/",
            "1250", "1000", "1", "0.5", "5", "1", "Training_GA", "1000_Gen")


# Determine Best Mutation Rate ============
elif testSet is 3:

    # 0
    runTest("0.0Mut", "Determine Best Settings/Mutation Rate/",
            "1250", "100", "1", "0.0", "5", "1", "Training_GA", "0_0_Mut")

    # 0.10
    runTest("0.10Mut", "Determine Best Settings/Mutation Rate/",
            "1250", "100", "1", "0.1", "5", "1", "Training_GA", "0_1_Mut")

    # 0.25
    runTest("0.25Mut", "Determine Best Settings/Mutation Rate/",
            "1250", "100", "1", "0.25", "5", "1", "Training_GA", "0_25_Mut")

    # 0.5
    runTest("0.5Mut", "Determine Best Settings/Mutation Rate/",
            "1250", "100", "1", "0.5", "5", "1", "Training_GA", "0_5_Mut")

    # 1.0
    runTest("1.0Mut", "Determine Best Settings/Mutation Rate/",
            "1250", "100", "1", "1.0", "5", "1", "Training_GA", "1_0_Mut")


# Determine Best Elitist Pool =============
elif testSet is 4:

    # 0
    runTest("0Elite", "Determine Best Settings/Elitist Pool/",
            "1250", "100", "1", "0.5", "0", "1", "Training_GA", "0_Elite")

    # 2
    runTest("2Elite", "Determine Best Settings/Elitist Pool/",
            "1250", "100", "1", "0.5", "2", "1", "Training_GA", "2_Elite")

    # 5
    runTest("5Elite", "Determine Best Settings/Elitist Pool/",
            "1250", "100", "1", "0.5", "5", "1", "Training_GA", "5_Elite")

    # 10
    runTest("10Elite", "Determine Best Settings/Elitist Pool/",
            "1250", "100", "1", "0.5", "10", "1", "Training_GA", "10_Elite")

    # 25
    runTest("25Elite", "Determine Best Settings/Elitist Pool/",
            "1250", "100", "1", "0.5", "25", "1", "Training_GA", "25_Elite")

# Iteration Comparison ====================
elif testSet is 5:

    # 1 - Only one test
    runTest("1Iter", "Multiple Iterations/",
            "1250", "100", "1", "0.5", "5", "1", "Training_GA", "1_Iter")

    # 2
    runTest("2Iter", "Multiple Iterations/",
            "1250", "100", "2", "0.5", "5", "1", "Training_GA", "2_Iter")

    # 5
    runTest("5Iter", "Multiple Iterations/",
            "1250", "100", "5", "0.5", "5", "1", "Training_GA", "5_Iter")

    # 10
    runTest("10Iter", "Multiple Iterations/",
            "1250", "100", "10", "0.5", "5", "1", "Training_GA", "10_Iter")

    # 20 - 20 Tests combined
    runTest("20Iter", "Multiple Iterations/",
            "1250", "100", "20", "0.5", "5", "1", "Training_GA", "20_Iter")

elif testSet is 6:

    # Bitstring Length Comparison =============

    # One Test With the Best Settings
    runTest("BSLen", "Bitstring Length/",
            "1250", "100", "1", "0.5", "5", "36", "Length_Training_GA", "BS_Len")

    # =========================================


log.close()
shutil.move("Results/OVERALL_TEST_RESULTS", "../Test Results/Genetic Algorithm/")