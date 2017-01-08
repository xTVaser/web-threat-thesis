import os
import re

os.chdir(os.getcwd())

fileOne = open("mysql_keywords_reserved")
existingKeywords = open("oracle_sql_keywords")
existingReserved = open("oracle_sql_reserved_words")

newKeywords = open("new_mysql_keywords", "w+")
newReserved = open("new_mysql_reserved", "w+")

keywords = []
reserved = []

for line in existingKeywords:
    keywords.append(line.replace("\n", ""))

for line in existingReserved:
    reserved.append(line.replace("\n", ""))

keywordContents = []
reservedContents = []

for line in fileOne:
    lineContents = line.split()

    for word in lineContents:
        if word.replace("(R)", "") in keywords or word.replace("(R)", "") in reserved:
            continue

        if "(R)" in word:
            reservedContents.append(word.replace("(R)", ""))
        else:
            keywordContents.append(word)

keywordContents.insert(0, "---")
reservedContents.insert(0, "---")

for i in range(len(keywordContents)-1):

    for j in range(len(keywordContents)-1):

        if i is j:
            continue

        if keywordContents[i] in keywordContents[j]:

            tempString = keywordContents.pop(i)
            keywordContents.insert(0, tempString)


for word in keywordContents:
    newKeywords.write(word + "\n")

for i in range(len(reservedContents)-1):

    for j in range(len(reservedContents)-1):

        if i is j:
            continue

        if reservedContents[i] in reservedContents[j]:

            tempString = reservedContents.pop(i)
            reservedContents.insert(0, tempString)


for word in reservedContents:
    newReserved.write(word + "\n")

newKeywords.close()
newReserved.close()