from operator import itemgetter
from random import uniform

from Lib.Request import *


# Returns the first 30% of the file as the trainingSet and the rest as the testingSet
def convertRequests(file):

    num_lines = sum(1 for line in open(file)) / 4
    trainingSet = []
    testingSet = []

    requests = open(file)

    for x in range(int(num_lines * 0.30)):

        request = requests.readline().replace("\n", "")
        sql = requests.readline().replace("\n", "")
        xss = requests.readline().replace("\n", "")
        rfi = requests.readline().replace("\n", "")

        temp = Request(request, sql, xss, rfi)
        trainingSet.append(temp)

    for x in range(int(num_lines * 0.70)):

        request = requests.readline().replace("\n", "")
        sql = requests.readline().replace("\n", "")
        xss = requests.readline().replace("\n", "")
        rfi = requests.readline().replace("\n", "")

        temp = Request(request, sql, xss, rfi)
        testingSet.append(temp)

    requests.close()

    return [trainingSet, testingSet]

# Return the bitstrings with attack type as pairs
def getBitstringColumn(index, bitstrings, type):

    output = []

    for bitstring in bitstrings:

        tempList = []

        # SQL
        if type is 1:
            tempList = bitstring.sql_bitstrings
        # XSS
        elif type is 2:
            tempList = bitstring.xss_bitstrings
        # RFI
        else:
            tempList = bitstring.rfi_bitstrings


        # Bitstring and fitness at 0 at the moment
        output.append((tempList[index], 0, int(bitstring.attackType)))

    return output

# Takes in a sorted bitstring set and normalizes them, the lowest remains the lowest, the highest remains the highest
def normalizeBitstrings(population):

    lowest = population[len(population)-1][1]
    # Add this amount to everything
    scaleFactor = (abs(lowest) * 2) + 1
    index = 0

    for individual in population:

        population[index] = (individual[0], individual[1]+scaleFactor, individual[2])
        index += 1


# Update the fitness value on each one, print out results here about the current results.
def evaluateFitness(population, testSet, type, iteration):

    index = 0

    # Loop through all individuals and evaluate their fitness
    for individual in population:

        correctDetected = 0
        falsePositive = 0
        incorrectDetected = 0 # Attack but not the right type, less of a penalty

        for test in testSet:

            if individual[0] == test[0]:

                # We dont care if the detection bitstring's original type is correct as its just a signature
                # We care about whether or not the bitstring we've identified is actually the attacks we are looking for
                if test[2] == type:
                    correctDetected += 1
                # If the detected bitstring is actually a normal request, then its a false positive.
                elif test[2] == 0:
                    falsePositive += 1
                # Otherwise, we detected another type of attack, but thought it was our type
                else:
                    incorrectDetected += 1

        # Store the fitness value
        # Number of correct detections divided by the total number of attacks in the test MINUS
        # Number of False positives divided by total number of normal requests (100% false positives = 0 fitness) MINUS
        # Number of incorrect detections, divided by total number, then eighth (less worse than false positives)
        # Then the entire thing is multipled by 100 to give it a bit more scale.
        fitness = (correctDetected/300) - (falsePositive/100) - (incorrectDetected/600)*0.125
        fitness *= 100

        population[index] = (individual[0], fitness, individual[2])
        index += 1

    # Sort the list based on the fitness, highest to lowest.
    population = sorted(population, key=itemgetter(1), reverse=True)

    normalizeBitstrings(population)

    print("Iteration: " + str(iteration) + " Maximum Fitness: " + str(population[0][1]) +
          " Minimum Fitness: " + str(population[len(population)-1][1]) +
          " Average Fitness: " + str(sumFitness(population) / len(population)))

    return population

# Just sums the fitness values in the population
def sumFitness(population):

    sum = 0

    for individual in population:

        sum += individual[1]

    return sum

# Returns the index of which individual choosen for selection
def rouletteSelect(fitnessSum, population):

    # Get the random value to search
    rndValue = uniform(0.0, 1.0) * fitnessSum

    index = 0

    for individual in population:

        # Subtract the fitness value
        rndValue -= individual[1]
        if rndValue <= 0:
            # Return the index
            return index
        index += 1

    # Something went wrong, just return the last item
    return len(population) - 1

def singlePointCrossover(offspring, parentOne, parentTwo):

    # Find the segment to swap, 0->3
    rndPoint = int(uniform(0, 4))

    # Take out the segments that are of interest
    parentOneContribution = parentOne[0][rndPoint]
    parentTwoContribution = parentTwo[0][rndPoint]

    # Swap the segments from either one
    alterParentOne = parentOne[0]
    alterParentOne[rndPoint] = parentTwoContribution

    alterParentTwo = parentTwo[0]
    alterParentTwo[rndPoint] = parentOneContribution

    # Create new tuples of them, swap the attacktypes but it really doesnt matter, as this is just a signature.
    newChild = (alterParentOne, 0, parentOne[2])
    newChild2 = (alterParentTwo, 0, parentTwo[2])

    # Add to the offspring list
    offspring.append(newChild)
    offspring.append(newChild2)

def reverse(bit):

    if bit is "0":
        return "1"
    else:
        return "0"

def mutatePopulation(population, mutationRate):

    index = 0
    for individual in population:

        tempSegment = []
        for segment in individual[0]:

            tempList = ""
            for bit in segment:

                # See if we will mutate or not
                mutateChance = round(uniform(0, 100), 2)

                if mutateChance < mutationRate:

                    tempList += reverse(bit)

                else:

                    tempList += bit

            tempSegment.append(tempList)

        # Update the bitstring
        population[index] = (tempSegment, population[index][1], population[index][2])
        index += 1

def bitstringLength(bitstring):

    output = ""

    for segment in bitstring:

        segmentLength = 0

        for bit in segment:

            segmentLength += 1

        output += str(segmentLength)

    return output

def tupleToString(tuple):

    output = ""

    for segment in tuple[0]:

        output += segment + " "

    return output