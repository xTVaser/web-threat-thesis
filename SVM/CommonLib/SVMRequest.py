import re

class SVMRequest(object):

    def __init__(self, request, sql, xss, rfi):

        self.info = []

        firstLine = request.split()
        self.request = firstLine[1]
        self.attackType = int(firstLine[0])

        secondLine = re.findall(r"\d+", sql)
        self.info.append( (int(secondLine[0]), int(secondLine[1])) )

        thirdLine = re.findall(r"\d+", xss)
        self.info.append( (int(thirdLine[0]), int(thirdLine[1])) )

        fourthLine = re.findall(r"\d+", rfi)
        self.info.append( (int(fourthLine[0]), int(fourthLine[1])) )


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

def grabInfoFromRequest(requests, infoSet, targetSet, index, correctType):

    for request in requests:
        infoSet.append(request.info[index])
    if correctType is False:
        targetSet += [0] * len(requests)
    else:
        targetSet += [1] * len(requests)

def getTestingSet(type, directory):

    return getTrainingSet(1500, 1500, 1500, 500, type, directory)


def getTrainingSet(numSQL, numXSS, numRFI, numNT, type, directory):

    infoSet = []
    targetSet = []

    # 1500/1500/1500/500
    sqlRequests = getRequests(directory + "SQL_SVM", numSQL)
    xssRequests = getRequests(directory + "XSS_SVM", numXSS)
    rfiRequests = getRequests(directory + "RFI_SVM", numRFI)
    ntRequests = getRequests(directory + "NT_SVM", numNT)

    grabInfoFromRequest(sqlRequests, infoSet, targetSet, type - 1, type == 1)
    grabInfoFromRequest(xssRequests, infoSet, targetSet, type - 1, type == 2)
    grabInfoFromRequest(rfiRequests, infoSet, targetSet, type - 1, type == 3)
    grabInfoFromRequest(ntRequests, infoSet, targetSet, type - 1, type == 0)

    return (infoSet, targetSet)






































