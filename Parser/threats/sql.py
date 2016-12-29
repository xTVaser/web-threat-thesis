import os
import re

reservedWordFile = open("../assets/sql_reserved.txt", "r")
keywordFile = open("../assets/sql_keywords.txt", "r")

keys = [];
for line in reservedWordFile.readlines():
    for word in line.split(","):
        keys.append(word.strip())

for line in keywordFile.readlines():
    for word in line.split(","):
        keys.append(word.strip())

print(keys)

#loop through request file.
requests = open("../testing/Bitstrings/sql_Small", "r")
tempFile = open("../testing/Bitstrings/sql_Small.tmp", "w")

#search for hexadecimal and ascii encodings of keywords as well.
lines = requests.readlines()

count = 0
numfields = 0
encodedFlag = False
for line in lines:
    for key in keys:
        if key in line:
            count += 1
    # limit size of counter
    if count > 7:
        count = 7

    fields = line.split("&")

    for field in fields:
        if "=" in field:
            for key in keys:
                if key in field:
                    numfields += 1


    if re.search("\%{1}([a-fA-F]|[0-9])*", line) is not None:
        encodedFlag = True

    if numfields > 7:
        numfields = 7

    tempFile.write(line.replace("\n", "") + "\t" + bin(count)[2:].zfill(3) + "" + str(int(encodedFlag)) + "" + bin(numfields)[2:].zfill(3) + "\n")
    count = 0
    numfields = 0
    encodedFlag = False