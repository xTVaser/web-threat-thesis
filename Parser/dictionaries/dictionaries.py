import os

def getHtmlTags():

    os.chdir(os.getcwd())

    file = open("html_tags")
    contents = []

    for line in file:
        contents.append(line)

    return contents


def getSqlKeywords():

    os.chdir(os.getcwd())

    file = open("sql_keywords")
    contents = []

    for line in file:
        contents.append(line)

    return contents


def getSqlReservedWords():

    os.chdir(os.getcwd())

    file = open("sql_reserved_words")
    contents = []

    for line in file:
        contents.append(line)

    return contents