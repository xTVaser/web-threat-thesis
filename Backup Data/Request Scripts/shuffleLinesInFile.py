import os, random

os.chdir(os.getcwd())

sqlFile = open("SQL_Testing")
xssFile = open("XSS_Testing")

newSqlFile = open("sqlInjections_new", "w+")
newXssFile = open("xssAttacks_new", "w+")

sqlLines = []
xssLines = []

for line in sqlFile:
    sqlLines.append(line)

for line in xssFile:
    xssLines.append(line)

random.shuffle(sqlLines)
random.shuffle(xssLines)

for line in sqlLines:
    newSqlFile.write(line)

for line in xssLines:
    newXssFile.write(line)