import re
from CommonLib import decodeURL
from dictionaries.getDictionaries import getSqlKeywords, getSqlKeywordsPreSuf, getSqlReservedWords, getSqlReservedWordsPreSuf


def sqlBitstringSVM(request):
    print("ye")

def getNumberSQLKeywords(workingRequest):

    keywordsPreSuf = getSqlKeywordsPreSuf()
    reservedWordsPreSuf = getSqlReservedWordsPreSuf()

    totalKeywords = 0

    # This can be put in a method, but will do later

    for line in keywordsPreSuf:

        keywords = line.split(" ")
        uniqueKeywords = 0

        regexResults = re.findall("[^A-Za-z{]" + keywords[0] + "[^A-Za-z}]", workingRequest.upper())
        keywordCount = len(regexResults)

        if keywordCount > 0 and len(keywords) > 1:

            for x in range(len(keywords) - 1):
                regexResults = re.findall("[^A-Za-z{]" + keywords[x + 1] + "[^A-Za-z}]", workingRequest.upper())
                uniqueKeywords += len(regexResults)

        keywordCount -= uniqueKeywords
        if keywordCount > 0:
            totalKeywords += keywordCount

    totalReservedWords = 0

    for line in reservedWordsPreSuf:

        keywords = line.split(" ")
        uniqueKeywords = 0

        # Avoids picking up normal words as requests
        regexResults = re.findall("[^A-Za-z{]" + keywords[0] + "[^A-Za-z}]", workingRequest.upper())
        keywordCount = len(regexResults)

        if keywordCount > 0 and len(keywords) > 1:

            for x in range(len(keywords) - 1):
                regexResults = re.findall("[^A-Za-z{]" + keywords[x + 1] + "[^A-Za-z}]", workingRequest.upper())
                uniqueKeywords += len(regexResults)

        keywordCount -= uniqueKeywords
        if keywordCount > 0:
            totalReservedWords += keywordCount

    return totalKeywords + totalReservedWords

# First Segment - Number of SQL Keywords
# Second Segment - Encoded Character?
# Third Segment - Number of Fields with SQL Keyword
# Fourth Segment -  Attack Type
# Attack types are the following:
# 1 - Tautology Attack - Manipulating the Where condition to evaluate to true
# 2 - Piggy Backing - Using a semicolon to add on additiona sql statements, anything is possible.
# 3 - Union - Return data different from the intended one, uses the keyword UNION
# 4 - Blind SQL Injection - Used to get an indirect result from the database, will use things like 0=1 or 1=0 or 1=1 to see if something is vulnerable
# 5 - Timing Attack - Manipulates timing delays for dbms respones, particularly uses the WAITFOR keyword
# 6 - Stored Procedure - Attack the stored procedures inside the database, can be any of the other attacks, it just uses the stored
                       # procedures as a mechanism to function, no way to detect this from just the resets as it is after it has ran through dbms
# 0 - Fits none of the above
def sqlBitstring(request, isSVM):

    if isSVM is True:
        sqlBitstringSVM(request)

    workingRequest = decodeURL(request)
    segments = []

    segments.append(getNumberSQLKeywords(workingRequest))

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

            # Avoids picking up normal words as requests
            regexResults = re.findall("[^A-Za-z{]" + keyword + "[^A-Za-z}]", field.upper())
            keywordCount = len(regexResults)

            if keywordCount > 0:
                numFieldsWithKeyword += 1
                hasKeyword = True
                break

        if hasKeyword is False:
            for keyword in simpleSqlReservedWords:

                # Avoids picking up normal words as requests
                regexResults = re.findall("[^A-Za-z{]" + keyword + "[^A-Za-z}]", field.upper())
                keywordCount = len(regexResults)

                if keywordCount > 0:
                    numFieldsWithKeyword += 1
                    break

    segments.append(numFieldsWithKeyword)


    # ATTACK TYPES
    # 1 - Tautology Attack - Manipulating the Where condition to evaluate to true

    tautologyFlag = False

    regexResults = re.findall("[^A-Za-z{]" + "WHERE" + "[^A-Za-z}]", workingRequest.upper())
    keywordCount = len(regexResults)

    if keywordCount > 0:
        tautologyFlag = True

    # 2 - Piggy Backing - Using a semicolon to add on additional sql statements, anything is possible.

    piggyBackingFlag = False
    fields = re.compile("(\?|&)[\w\d]+=").split(workingRequest)
    del fields[
        1::2]  # Get rid of every second element because the regex is fine but python adds non-existant characters?
    del fields[0]

    for field in fields:

        if ";" in field:

            # Check if there are SQL keywords on either sides of the semicolon
            subfields = field.split(";")

            fieldA = False
            fieldB = False
            counter = 1
            for subfield in subfields:

                if counter % 2 == 1 and getNumberSQLKeywords(subfield) < 0:
                    fieldA = True
                elif getNumberSQLKeywords(subfield) < 0:
                    fieldB = True

                if counter % 2 == 0 and fieldA is True and fieldB is True:
                    piggyBackingFlag = True
                else:
                    fieldA = False
                    fieldB = False


    # 3 - Union - Return data different from the intended one, uses the keyword UNION

    unionFlag = False

    regexResults = re.findall("[^A-Za-z{]" + "UNION" + "[^A-Za-z}]", workingRequest.upper())
    keywordCount = len(regexResults)

    if keywordCount > 0:
        unionFlag = True


    # 4 - Blind SQL Injection - Used to get an indirect result from the database, will use things like 0=1 or 1=0 or 1=1 to see if something is vulnerable

    blindFlag = False
    regexResults = re.findall("(1|0)=(1|0)", workingRequest.upper())

    if len(regexResults) > 0:
        blindFlag = True

    # 5 - Timing Attack - Manipulates timing delays for dbms respones, particularly uses the WAITFOR keyword

    timingFlag = False
    regexResults = re.findall("[^A-Za-z{]" + "WAITFOR" + "[^A-Za-z}]", workingRequest.upper())
    keywordCount = len(regexResults)

    if keywordCount > 0:
        timingFlag = True


    if piggyBackingFlag is True:
        segments.append(2)
    elif timingFlag is True:
        segments.append(5)
    elif blindFlag is True:
        segments.append(4)
    elif unionFlag is True:
        segments.append(3)
    elif tautologyFlag is True:
        segments.append(1)
    # 0 - Fits none of the above
    else:
        segments.append(0)

    return segments