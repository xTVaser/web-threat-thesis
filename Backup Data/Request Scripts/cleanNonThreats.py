import os, random

os.chdir(os.getcwd())

file = open("NT_Training")

newFile = open("NT_Training_New", "w+")

lines = []

for line in file:
    contents = line.split()

    requestLine = contents[len(contents)-1]

    newRequestLine = "/test/website"
    urlParams = requestLine.split("/")

    for x in range(len(urlParams)-3):
        newRequestLine += "/" + urlParams[x+3]

    lines.append(newRequestLine)


distinctLines = list(set(lines))
random.shuffle(distinctLines)

for line in distinctLines:
    newFile.write(line + "\n")