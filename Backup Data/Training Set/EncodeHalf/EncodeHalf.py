import os
from random import randint
from urllib import parse
import re

def decodeURL(url):

    # Get rid of any padded zeros first
    paddedEncoded = re.findall("%0+[0-9A-Fa-f]{2}", url)

    for problem in paddedEncoded:

        newEncode = ""

        numberBegins = False
        for c in problem:
            if c == '%' and numberBegins is False:
                newEncode += c
            elif c != '0':
                numberBegins = True
            if numberBegins is True:
                newEncode += c

        url = url.replace(problem, newEncode)

    # Get rid of any decimal number trickery as well
    decimalEncoded = re.findall("%[0-9A-Fa-f]{2}\.[\dx*-]+", url)

    for problem in decimalEncoded:

        newEncode = ""

        for c in range(len(problem)-1):

            if c <= 2:
                newEncode += problem[c]

        url = url.replace(problem, newEncode)

    return parse.unquote(url)

os.chdir(os.getcwd())

sqlFile = open("SQL_Training")
xssFile = open("XSS_Training")

newSqlFile = open("SQL_Training_New", "w+")

coin = randint(0, 1)

for line in sqlFile:

    if coin is 0:
        newSqlFile.write(decodeURL(line.replace("\n", "")) + "\n")
    else:
        newSqlFile.write(line.replace("\n", "") + "\n")
    coin = randint(0, 1)

for line in xssFile:

    if coin is 0:
        request = decodeURL(line.replace("\n", ""))
        print(request)
    else:
        request = line.replace("\n", "")
        print(request)
    coin = randint(0, 1)

newSqlFile.close()
