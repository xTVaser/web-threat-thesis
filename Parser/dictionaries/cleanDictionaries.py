import os

os.chdir(os.getcwd())

fileOne = open("sql_keywords")
fileTwo = open("sql_reserved")
fileThree = open("html_tags")

newFileOne = open("new_sql_keywords", "w+")
newFileTwo = open("new_sql_reserved", "w+")
newFileThree = open("new_html_tags", "w+")

fileOneContents = []
fileTwoContents = []
fileThreeContents = []

for line in fileOne:
    lineContents = line.split(", ")

    for word in lineContents:
        fileOneContents.append(word.replace("\n", ""))

for line in fileTwo:
    lineContents = line.split(", ")

    for word in lineContents:
        fileTwoContents.append(word.replace("\n", ""))

for line in fileThree:
    fileThreeContents.append(line.replace("\n", ""))

#Take any word that is a prefix for another word, and place it near the top of the list so i know which ones to
#Pay attention to later on.

delimiterLine = 0

for i in range(len(fileOneContents)-1):

    for j in range(len(fileOneContents)-1):

        if i is j:
            continue

        if fileOneContents[j].startswith(fileOneContents[i]):

            tempString = fileOneContents.pop(i)
            fileOneContents.insert(0, tempString)
            delimiterLine += 1

fileOneContents.insert(delimiterLine, "---")
delimiterLine = 0

for i in range(len(fileTwoContents) - 1):

    for j in range(len(fileTwoContents) - 1):

        if i is j:
            continue

        if fileTwoContents[j].startswith(fileTwoContents[i]):
            tempString = fileTwoContents.pop(i)
            fileTwoContents.insert(0, tempString)
            delimiterLine += 1

fileTwoContents.insert(delimiterLine, "---")
delimiterLine = 0

for i in range(len(fileThreeContents) - 1):

    for j in range(len(fileThreeContents) - 1):

        if i is j:
            continue

        if fileThreeContents[j].startswith(fileThreeContents[i]):
            tempString = fileThreeContents.pop(i)
            fileThreeContents.insert(0, tempString)
            delimiterLine += 1

fileThreeContents.insert(delimiterLine, "---")

for word in fileOneContents:
    newFileOne.write(word + "\n")

for word in fileTwoContents:
    newFileTwo.write(word + "\n")

for word in fileThreeContents:
    newFileThree.write(word + "\n")
