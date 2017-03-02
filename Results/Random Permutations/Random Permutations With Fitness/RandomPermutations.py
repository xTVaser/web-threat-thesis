from RandomRequest import *
import os
from operator import attrgetter

def printBinary(s1, s2, s3, s4):

    output = [bin(s1)[2:].zfill(6)] + \
             [bin(s2)[2:].zfill(1)] + \
             [bin(s3)[2:].zfill(6)] + \
             [bin(s4)[2:].zfill(3)]

    return output

def generatePermutations(type):

    permutations = []

    for s1 in range(64): # 6 bits

        for s2 in range(2): # 1 bit

            for s3 in range(64): # 6 bits

                for s4 in range(8): # 3 bits

                    if (type == 1):
                        permutations.append(RandomRequest("1 Test_Permutation", printBinary(s1, s2, s3, s4), None, None))
                    elif (type == 2):
                        permutations.append(RandomRequest("2 Test_Permutation", None, printBinary(s1, s2, s3, s4), None))
                    elif (type == 3):
                        permutations.append(RandomRequest("3 Test_Permutation", None, None, printBinary(s1, s2, s3, s4)))

    return permutations


# Update the fitness value on each one, print out results here about the current results.
def fitnessRemoval(permutations, training, type):

    printIndex = 0

    importantPermutations = []


    # Loop through all individuals and evaluate their fitness
    for permutation in permutations:

        # indexes: 0 - correct, 1 - false positives, 2 - incorrect detections
        statistics = [0,0,0]

        for test in training:

            trainingSignature = []
            matchingSignature = []

            if (type == 1):
                trainingSignature = test.sql
                matchingSignature = permutation.sql
            elif (type == 2):
                trainingSignature = test.xss
                matchingSignature = permutation.xss
            elif (type == 3):
                trainingSignature = test.rfi
                matchingSignature = permutation.rfi

            if trainingSignature == matchingSignature:

                if str(permutation.attackType) == str(test.attackType):
                    statistics[0] += 1
                elif str(test.attackType) == "0":
                    statistics[1] += 1
                else:
                    statistics[2] += 1

        # Store the fitness value
        # Number of correct detections divided by the total number of attacks in the test MINUS
        # Number of False positives divided by total number of normal requests (100% false positives = 0 fitness) MINUS
        # Number of incorrect detections, divided by total number, then eighth (less worse than false positives)
        # Then the entire thing is multipled by 100 to give it a bit more scale.
        fitness = (statistics[0]/300) - (statistics[1]/100) - (statistics[2]/600)*0.125
        fitness *= 100

        if statistics != [0,0,0]:
            permutation.setFitness(fitness)
            importantPermutations.append(permutation)

        print(printIndex)
        printIndex += 1

    # Sort the list based on the fitness, highest to lowest.
    importantPermutations = sorted(importantPermutations, key=attrgetter('fitness'), reverse=True)

    return importantPermutations


def getSignature(line):

    return line.split()[1].split(".")

def randomPermutations(type, training, testing):

    # Make random permutation of every single possible bitstring
    permutations = generatePermutations(type)

    # Get training set

    trainingFile = open(training).readlines()
    trainingSet = []
    lineIndex = 0

    while lineIndex < len(trainingFile):

        sqlSignature = getSignature(trainingFile[lineIndex+1])
        xssSignature = getSignature(trainingFile[lineIndex+2])
        rfiSignature = getSignature(trainingFile[lineIndex+3])
        newRequest = RandomRequest(trainingFile[lineIndex], sqlSignature, xssSignature, rfiSignature)

        lineIndex += 4
        trainingSet.append(newRequest)

    # Test fitness against the training set
    permutations = fitnessRemoval(permutations, trainingSet, type)

    testingFile = open(testing).readlines()
    testingSet = []
    lineIndex = 0

    while lineIndex < len(testingFile):

        sqlSignature = getSignature(testingFile[lineIndex + 1])
        xssSignature = getSignature(testingFile[lineIndex + 2])
        rfiSignature = getSignature(testingFile[lineIndex + 3])
        newRequest = RandomRequest(testingFile[lineIndex], sqlSignature, xssSignature, rfiSignature)

        testingSet.append(newRequest)
        lineIndex += 4

    for test in [20, 40, 60, 80, 100]:

        print(test)

        numKeep = len(permutations) * test/100.0
        currentPermutations = permutations[:int(numKeep)]

        # Test with testing set

        # indexes: 0 - correct, 1 - false positives, 2 - incorrect detections
        statistics = [0, 0, 0]
        successfulDetection = False
        falsePositiveFlag = False
        wrongDetection = False

        for potentialAttack in testingSet:

            for signature in currentPermutations:

                testingSignature = []
                matchingSignature = []

                if (type == 1):
                    testingSignature = potentialAttack.sql
                    matchingSignature = signature.sql
                elif (type == 2):
                    testingSignature = potentialAttack.xss
                    matchingSignature = signature.xss
                elif (type == 3):
                    testingSignature = potentialAttack.rfi
                    matchingSignature = signature.rfi

                if testingSignature == matchingSignature and str(potentialAttack.attackType) == str(type):

                    statistics[0] += 1
                    successfulDetection = True
                    break

                elif testingSignature == matchingSignature and str(potentialAttack.attackType) == "0":

                    statistics[1] += 1
                    falsePositiveFlag = True
                    break

                elif testingSignature == matchingSignature and str(potentialAttack.attackType) != str(type):

                    wrongDetection = True

            # If we wrong detect, we give it a chance to either false positive or find the proper bitstring b
            # but if it still was unable, then it was a false detection
            if wrongDetection is True and falsePositiveFlag is False and successfulDetection is False:
                statistics[2] += 1

            successfulDetection = False
            falsePositiveFlag = False
            wrongDetection = False


        statistics = [statistics[0]/1500*100, statistics[1]/3000*100, statistics[2]/500*100]

        sqlResults = None
        xssResults = None
        rfiResults = None

        if os.path.exists("Results_SQL.res"):
            sqlResults = open("Results_SQL.res", "a")
            xssResults = open("Results_XSS.res", "a")
            rfiResults = open("Results_RFI.res", "a")
        else:
            sqlResults = open("Results_SQL.res", "w+")
            xssResults = open("Results_XSS.res", "w+")
            rfiResults = open("Results_RFI.res", "w+")

        if type == 1:
            sqlResults.write(str(test) + "\t" + str(statistics[0]) + "\t" + str(statistics[1]) + "\t" + str(statistics[2]) + "\n")
        elif type == 2:
            xssResults.write(str(test) + "\t" + str(statistics[0]) + "\t" + str(statistics[1]) + "\t" + str(statistics[2]) + "\n")
        else:
            rfiResults.write(str(test) + "\t" + str(statistics[0]) + "\t" + str(statistics[1]) + "\t" + str(statistics[2]) + "\n")

        sqlResults.close()
        xssResults.close()
        rfiResults.close()


randomPermutations(1, "Training_GA", "Testing_GA")
randomPermutations(2, "Training_GA", "Testing_GA")
randomPermutations(3, "Training_GA", "Testing_GA")
