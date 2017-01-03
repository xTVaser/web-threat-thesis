import re
from CommonLib import decodeURL
from dictionaries.getDictionaries import getSqlKeywords, getSqlKeywordsPreSuf, getSqlReservedWords, getSqlReservedWordsPreSuf


def sqlBitstringSVM(request):
    print("ye")


# First Segment - Number of SQL Keywords
# Second Segment - Encoded Character?
# Third Segment - Number of Fields with SQL Keyword
# Fourth Segment -  Attack Type
# Attack types are the following:
# 1 - Tautology Attack -
# 2 - Piggy Backing -
# 3 - Union -
# 4 - Stored Procedure -
# 5 - Bling SQL Injection -
# 6 - Timing Attack -
# 0 - Fits none of the above -
def sqlBitstring(request, isSVM):

    if isSVM is True:
        sqlBitstringSVM(request)

    workingRequest = decodeURL(request)
    segments = []

    keywordsPreSuf = getSqlKeywordsPreSuf()
    reservedWordsPreSuf = getSqlReservedWordsPreSuf()

    totalKeywords = 0

    # This can be put in a method, but will do later

    for line in keywordsPreSuf:

        keywords = line.split(" ")
        uniqueKeywords = 0

        keywordCount = workingRequest.upper().count(keywords[0])

        if keywordCount > 0 and len(keywords) > 1:

            for x in range(len(keywords) - 2):
                uniqueKeywords += workingRequest.upper().count(keywords[x + 1])

        keywordCount -= uniqueKeywords
        if keywordCount > 0:
            totalKeywords += keywordCount

    totalReservedWords = 0

    for line in reservedWordsPreSuf:

        keywords = line.split(" ")
        uniqueKeywords = 0

        keywordCount = workingRequest.upper().count(keywords[0])

        if keywordCount > 0 and len(keywords) > 1:

            for x in range(len(keywords) - 2):
                uniqueKeywords += workingRequest.upper().count(keywords[x + 1])

        keywordCount -= uniqueKeywords
        if keywordCount > 0:
            totalReservedWords += keywordCount

    segments.append(totalKeywords)


    # Encoded Characters
    if workingRequest != request:
        segments.append(1)
    else:
        segments.append(0)



    # ATTACK TYPES


    return segments