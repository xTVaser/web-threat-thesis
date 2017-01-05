import os, random

os.chdir(os.getcwd())

# sqlFile = open("SQL_Testing")
# xssFile = open("XSS_Testing")
rfiFile = open("rfiAttacks")

# newSqlFile = open("sqlInjections_new", "w+")
# newXssFile = open("xssAttacks_new", "w+")
newRfiFile = open("rfiAttacks_new", "w+")

sqlLines = []
xssLines = []
rfiLines = []

# for line in sqlFile:
#     sqlLines.append(line)
#
# for line in xssFile:
#     xssLines.append(line)

for line in rfiFile:
    rfiLines.append(line)

# random.shuffle(sqlLines)
# random.shuffle(xssLines)
random.shuffle(rfiLines)

# for line in sqlLines:
#     newSqlFile.write(line)
#
# for line in xssLines:
#     newXssFile.write(line)

for line in rfiLines:
    newRfiFile.write(line)