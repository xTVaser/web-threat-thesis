import os

dir = "/home/tyler/Repos/My Repositories/thesis2016/Parser/dictionaries/"

# Returning the tags in a special way so that we wont do any double counting
def getHtmlTagsPreSuf():
    

# Remove the delimiter
def getHtmlTags():

    os.chdir(dir)

    file = open("html_tags")
    contents = []

    for line in file:
        contents.append(line.replace("\n", ""))

    return contents


def getSqlKeywords():

    os.chdir(dir)

    file = open("sql_keywords")
    contents = []

    for line in file:
        contents.append(line.replace("\n", ""))

    return contents


def getSqlReservedWords():

    os.chdir(dir)

    file = open("sql_reserved_words")
    contents = []

    for line in file:
        contents.append(line.replace("\n", ""))

    return contents

def getDOM():

    os.chdir(dir)

    file = open("dom_method")
    contents = []

    for line in file:
        contents.append(line.replace("\n", ""))

    return contents

def getDOMEventListeners():

    os.chdir(dir)

    file = open("dom_eventlisteners")
    contents = []

    for line in file:
        contents.append(line.replace("\n", ""))

    return contents

def getDOMAttributes():

    os.chdir(dir)

    file = open("dom_attributes")
    contents = []

    for line in file:
        contents.append(line.replace("\n", ""))

    return contents