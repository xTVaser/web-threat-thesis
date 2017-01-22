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
