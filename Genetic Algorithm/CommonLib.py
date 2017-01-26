from Request import *
from operator import itemgetter

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

# Update the fitness value on each one, print out results here about the current results.
def evaluateFitness(population, testSet, type):

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
        # Number of incorrect detections, divided by total number, then halfed (less worse than false positives)
        # Then the entire thing is multipled by 100 to give it a bit more scale.
        fitness = (correctDetected/300) - (falsePositive/100) - (incorrectDetected/600)*0.5
        fitness *= 100

        if fitness < 0:
            fitness = 0

        population[index] = (individual[0], fitness, individual[2])
        index += 1

    # Sort the list based on the fitness, highest to lowest.
    population = sorted(population, key=itemgetter(1), reverse=True)

    return population