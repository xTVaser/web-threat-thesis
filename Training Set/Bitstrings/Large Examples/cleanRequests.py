import os

os.chdir(os.getcwd())

sqlFile = open("sqlInjections")
xssFile = open("xssAttacks")

newSqlFile = open("sqlInjections_new", "w+")
newXssFile = open("xssAttacks_new", "w+")

for line in sqlFile:
    contents = line.split(" ")
    if len(contents) is 3:
        newLine = contents[1].replace("/fab/memelords/", "/test/website/")
        if newLine != "/test/website/index.php":
            newSqlFile.write(newLine + "\n")

for line in xssFile:
    contents = line.split(" ")
    if len(contents) is 3:
        newLine = contents[1].replace("/fab/memelords/", "/test/website/")
        if newLine != "/test/website/index.php":
            newXssFile.write(newLine + "\n")