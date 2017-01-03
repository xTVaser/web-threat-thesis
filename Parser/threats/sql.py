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

        regexResults = re.findall("(?![^A-Za-z])" + keywords[0] + "(?=[^A-Za-z])", workingRequest.upper())
        keywordCount = len(regexResults)

        if keywordCount > 0 and len(keywords) > 1:

            for x in range(len(keywords) - 1):
                regexResults = re.findall("(?![^A-Za-z])" + keywords[x + 1] + "(?=[^A-Za-z])", workingRequest.upper())
                uniqueKeywords += len(regexResults)

        keywordCount -= uniqueKeywords
        if keywordCount > 0:
            totalKeywords += keywordCount

    totalReservedWords = 0

    for line in reservedWordsPreSuf:

        keywords = line.split(" ")
        uniqueKeywords = 0

        # Avoids picking up normal words as requests
        regexResults = re.findall("(?![^A-Za-z])" + keywords[0] + "(?=[^A-Za-z])", workingRequest.upper())
        keywordCount = len(regexResults)

        if keywordCount > 0 and len(keywords) > 1:

            for x in range(len(keywords) - 1):
                regexResults = re.findall("(?![^A-Za-z])" + keywords[x + 1] + "(?=[^A-Za-z])", workingRequest.upper())
                uniqueKeywords += len(regexResults)

        keywordCount -= uniqueKeywords
        if keywordCount > 0:
            totalReservedWords += keywordCount

    segments.append(totalKeywords + totalReservedWords)

    # Encoded Characters
    if workingRequest != request:
        segments.append(1)
    else:
        segments.append(0)

    # Number of Fields with SQL Keywords
    simpleSqlKeywords = getSqlKeywords()
    simpleSqlReservedWords = getSqlReservedWords()

    # Regex to match with all fields
    fields = re.compile("(\?|&)[\w\d]+=").split(workingRequest)
    del fields[1::2]  # Get rid of every second element because the regex is fine but python adds non-existant characters?
    del fields[0]  # Delete the first field because it isnt a field

    numFieldsWithKeyword = 0

    for field in fields:

        hasKeyword = False

        for keyword in simpleSqlKeywords:

            if keyword in field.upper():
                numFieldsWithKeyword += 1
                hasKeyword = True
                break

        if hasKeyword is False:
            for keyword in simpleSqlReservedWords:

                if keyword in field.upper():
                    numFieldsWithKeyword += 1
                    break

    segments.append(numFieldsWithKeyword)


    # ATTACK TYPES


    return segments