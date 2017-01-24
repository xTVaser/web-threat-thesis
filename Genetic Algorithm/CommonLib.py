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
def genAlgorithm(tranSet, testSet, maxPop, generations, selectPool, mutationRate, elitistPool, type, numBitstrings):

    globalResults = []

    # Deal with each "column" of bitstrings individually
    for b in range(numBitstrings):

        # Get only the bitstrings we care about, make pairs with the attack type
        trainingList = getBitstringColumn(b, tranSet)
        testingList = getBitstringColumn(b, testSet)

        # The training list is our initial population, the testing list is the original entire set, unaltered
        population = trainingList.copy()
        testingList += trainingList

        # Loop through all of the generations
        for g in range(generations):

            # Evaluate Fitness, at this point the bitstrings will become part of a triple (BS, Type, Fitness)
            evaluateFitness(population)

            offspring = []

            # Elitist Pool - Copy the top X% over to the offspring

            # Selection Loop - Produce offspring until we are at max population
            while len(offspring) < maxPop:

                # Selection Algorithm Here - Roulette Wheel Selection
                print("stub")

                # Individual 1
                # Individual 2
                # Breed them with a random single-point crossover and add the two offspring to the list

            # Remove any extra children over maxPop just incase
            offspring = offspring.split(maxPop)[0]

            # Mutation Loop
            for child in offspring:

                # Loop through all of the individual bits, and randomly mutate them
                print("stub")

        # Once all generations are complete, the current population is the best bitstrings we could generate
        globalResults.append(population)

    return globalResults