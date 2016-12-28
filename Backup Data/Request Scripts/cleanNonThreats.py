import os, random

os.chdir(os.getcwd())

file = open("nonthreats")

newFile = open("nonthreats_new", "w+")

lines = []

for line in file:
    contents = line.split(" ")
    if len(contents) is 3:
        newLine = contents[1].replace("/fab/memelords/", "/test/website/")
        lines.append(newLine + "\n")

distinctLines = list(set(lines))
random.shuffle(distinctLines)

for line in distinctLines:
    newFile.write(line)