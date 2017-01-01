import os

dir = "/home/tyler/Repos/My Repositories/thesis2016/Parser/dictionaries/"

# Returning the tags in a special way so that we wont do any double counting
def getHtmlTagsPreSuf():

    os.chdir(dir)

    file = open("html_tags")
    contents = []

    prefixTags = []
    suffixTags = []

    finishedPrefixes = False
    # Seperate the tags that are prefixes to other tags from the rest so we can not double count later on.
    for tag in file:
        if finishedPrefixes is False and tag != "---":
            prefixTags.append(tag.replace("\n", ""))
        if finishedPrefixes is True:
            suffixTags.append(tag.replace("\n", ""))
        if tag.replace("\n", "") == "---":
            finishedPrefixes = True

    # Syntax will be <tag> <list of tags that are suffixes to it>\n

    for suffix in suffixTags:
        contents.append(suffix)

    for prefix in prefixTags:
        line = prefix

        for suffix in suffixTags:

            if suffix.startswith(prefix):
                line += " " + suffix

        contents.append(line)

    return contents


# Remove the delimiter
def getHtmlTags():

    os.chdir(dir)

    file = open("html_tags")
    contents = []

    for line in file:
        if line != "---":
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