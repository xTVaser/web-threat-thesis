import re

class SVMRequest(object):

    def __init__(self, request, sql, xss, rfi):

        self.info = []

        firstLine = request.split()
        self.request = firstLine[1]
        self.attackType = int(firstLine[0])

        secondLine = re.findall(r"\d+", sql)
        self.info.append( (float(secondLine[0]), float(secondLine[1])) )

        thirdLine = re.findall(r"\d+", xss)
        self.info.append( (float(thirdLine[0]), float(thirdLine[1])) )

        fourthLine = re.findall(r"\d+", rfi)
        self.info.append( (float(fourthLine[0]), float(fourthLine[1])) )

    def __str__(self):
        return str(self.info)

def getRequests(file, n):

    requests = []
    lines = open(file, "r").readlines()
    index = 0

    while n > 0 and index < len(lines):

        req = SVMRequest(lines[index], lines[index+1], lines[index+2], lines[index+3])
        index += 4
        requests.append(req)
        n -= 1

    return requests

def grabInfoFromRequest(requests, infoSet, targetSet, index, correctType, removeDuplicates):

    if removeDuplicates is True:
        uniqueRequests = []

        # Remove duplicates from the request list as the complexity introduced in poly and rbf kernels is too great
        for request in requests:

            unique = True

            for uniqueRequest in uniqueRequests:

                if request.info[index] == uniqueRequest.info[index]:
                    unique = False
                    break

            if unique is True:
                uniqueRequests.append(request)

        requests = uniqueRequests

    for request in requests:
        infoSet.append(request.info[index])
    if correctType is False:
        targetSet += [0] * len(requests)
    else:
        targetSet += [1] * len(requests)

def getTestingSet(type, directory):

    # We dont care about the targets because we arent training with this.
    # Instead we want attack types
    requests = getTrainingSet(1500, 1500, 1500, 500, type, directory, False)
    attackTypes = [1] * 1500 + [2] * 1500 + [3] * 1500 + [0] * 500

    return (requests[0], attackTypes)


def getTrainingSet(numSQL, numXSS, numRFI, numNT, type, directory, removeDuplicates):

    infoSet = []
    targetSet = []

    # 1500/1500/1500/500
    sqlRequests = getRequests(directory + "SQL_SVM", numSQL)
    xssRequests = getRequests(directory + "XSS_SVM", numXSS)
    rfiRequests = getRequests(directory + "RFI_SVM", numRFI)
    ntRequests = getRequests(directory + "NT_SVM", numNT)

    grabInfoFromRequest(sqlRequests, infoSet, targetSet, type - 1, type == 1, removeDuplicates)
    grabInfoFromRequest(xssRequests, infoSet, targetSet, type - 1, type == 2, removeDuplicates)
    grabInfoFromRequest(rfiRequests, infoSet, targetSet, type - 1, type == 3, removeDuplicates)
    grabInfoFromRequest(ntRequests, infoSet, targetSet, type - 1, type == 0, removeDuplicates)

    return (infoSet, targetSet)
