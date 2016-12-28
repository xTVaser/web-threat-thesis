import os

os.chdir(os.getcwd())

sqlFile = open("sqlInjections")
xssFile = open("xssAttacks")

newSqlFile = open("sqlInjections_new", "w+")
newXssFile = open("xssAttacks_new", "w+")

for line in sqlFile:
    newLine = line.replace("meme", "post")
    newSqlFile.write(newLine)

for line in xssFile:
    newLine = line.replace("meme", "post")
    newXssFile.write(newLine)