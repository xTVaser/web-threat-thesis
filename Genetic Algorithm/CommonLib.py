from Request import *

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

# Return a list of a list of all resulting bitstrings for each bitstring length
def genAlgorithm(tranSet, testset, maxPop, generations, selectPool, mutationRate, elitistPool, type):

# This training set will go into a new list, but we test for fitness on the ENTIRE collection

# Evaluate all of the bitstrings using the genetic algorithm, and create new and delete unneeded ones based on fitness.


# Continue this until a stopping condition, such as a detection % is reached, or number of iterations is reached, or pop size, etc.

# Now training is complete, and our training array or list should contain a bunch of highly accurate bitstrings for detection.

# Add these bitstrings to a file that will be used later on