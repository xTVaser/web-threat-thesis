from more_itertools import unique_everseen

from Lib.CommonLib import evaluateFitness
from Lib.CommonLib import getBitstringColumn
from Lib.CommonLib import mutatePopulation
from Lib.CommonLib import rouletteSelect
from Lib.CommonLib import singlePointCrossover
from Lib.CommonLib import sumFitness


# Return a list of a list of all resulting bitstrings for each bitstring length
def genAlgorithm(tranSet, testSet, maxPop, generations, mutationRate, elitistPer, type, numBitstrings):

    globalResults = []

    # Deal with each "column" of bitstrings individually
    for b in range(numBitstrings):

        # Get only the bitstrings we care about,
        # We need the actual type to be stored alongside the bitstring for fitness evaluation
        trainingList = getBitstringColumn(b, tranSet, type)
        testingList = getBitstringColumn(b, testSet, type)

        # The training list is our initial population, remove any duplicate bitstrings to not inflate fitness values
        population = trainingList.copy()
        population = list(unique_everseen(population))
        # The testing list is the original entire set, unaltered
        testingList += trainingList

        # Loop through all of the generations
        for g in range(generations):

            # Remove Duplicates Before Continuing on
            population = list(unique_everseen(population))

            # Evaluate Fitness, at this point the bitstrings will become part of a triple (BS, Fitness, Type)
            population = evaluateFitness(population, testingList, type, g+1)

            offspring = []

            # Elitist Pool - Copy the top X% over to the offspring
            elitistAmount = len(population) * (elitistPer/100)
            for i in range(int(elitistAmount)):
                # Don't fill over the population size
                if len(offspring) < maxPop:
                    offspring.append(population[i])

            # Find the sum of the fitnesses once because it doesnt change everytime
            sumOfFitnesses = sumFitness(population)

            # Selection Loop - Produce offspring until we are at max population
            while len(offspring) < maxPop:

                # Roulette Wheel Selection
                # Individual 1
                firstIndividual = population[rouletteSelect(sumOfFitnesses, population)]
                # Individual 2
                secondIndividual = population[rouletteSelect(sumOfFitnesses, population)]

                # Breed them with a random single-point crossover and add the two offspring to the list
                singlePointCrossover(offspring, firstIndividual, secondIndividual)

            # Remove any extra children over maxPop just incase
            offspring = offspring[0:maxPop]

            # Mutation Loop
            mutatePopulation(offspring, mutationRate)

            # Now set the offspring to be our new population
            population = offspring

        # Once all generations are complete, the current population is the best bitstrings we could generate
        globalResults.append(population)

    # Now that these are supposed to be the best bitstrings to detect one of the three attacks,
    # we can remove the attack type info
    return globalResults