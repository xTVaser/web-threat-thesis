from CommonLib import getBitstringColumn
from CommonLib import evaluateFitness

# Return a list of a list of all resulting bitstrings for each bitstring length
def genAlgorithm(tranSet, testSet, maxPop, generations, selectPool, mutationRate, elitistPool, type, numBitstrings):

    globalResults = []

    # Deal with each "column" of bitstrings individually
    for b in range(numBitstrings):

        # Get only the bitstrings we care about,
        # We need the actual type to be stored alongside the bitstring for fitness evaluation
        trainingList = getBitstringColumn(b, tranSet, type)
        testingList = getBitstringColumn(b, testSet, type)

        # The training list is our initial population, the testing list is the original entire set, unaltered
        population = trainingList.copy()
        testingList += trainingList

        # Loop through all of the generations
        for g in range(generations):

            # Evaluate Fitness, at this point the bitstrings will become part of a triple (BS, Fitness, Type)
            population = evaluateFitness(population, testingList, type)

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

    # Now that these are supposed to be the best bitstrings to detect one of the three attacks,
    # we can remove the attack type info
    return globalResults

# selection rate - randomly select with the selection rate, fitness will give an edge.
# mutation rate - mutate across all bits of all individuals after selection and cross over.(usually between 1 and 2 tenths of a percent, but did they do that?)
# cross over rate - once you have the two chromosomes selected, the likely hood you will decide to cross them over.
#
# each cycle of selection and mutation/crossovering is called a generation, aka an iteration
# the children are what will pass onto the next generation and nothing else, there is a concept of selecting some "elite" ones and bringing them over, but we dont.
#
# Loop and generate new children until we reach the population, then go to the next generation after mutations until offspring == population size.