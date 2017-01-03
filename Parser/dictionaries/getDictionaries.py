import os

dir = "/home/tyler/Repos/My Repositories/thesis2016/Parser/dictionaries/"

def getPreSuf(filename):

    os.chdir(dir)

    file = open(filename)
    contents = []

    prefixTags = []
    suffixTags = []

    finishedPrefixes = False
    # Seperate the tags that are prefixes to other tags from the rest so we can not double count later on.
    for tag in file:
        if finishedPrefixes is False and tag.replace("\n", "") != "---":
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

# Very similar to the above method but the word can be anywhere within, not just a prefix.
def getKeywordsContains(filename):

    os.chdir(dir)

    file = open(filename)
    contents = []

    substrings = []
    wholestrings = []

    finishedSubstrings = False
    # Seperate the tags that are prefixes to other tags from the rest so we can not double count later on.
    for keyword in file:
        if finishedSubstrings is False and keyword.replace("\n", "") != "---":
            substrings.append(keyword.replace("\n", ""))
        if finishedSubstrings is True:
            wholestrings.append(keyword.replace("\n", ""))
        if keyword.replace("\n", "") == "---":
            finishedSubstrings = True

    # Syntax will be <tag> <list of tags that are suffixes to it>\n

    for string in wholestrings:
        contents.append(string)

    for substring in substrings:
        line = substring

        for string in wholestrings:

            if substring in string:
                line += " " + string

        contents.append(line)

    return contents

# Returning the tags in a special way so that we wont do any double counting
def getHtmlTagsPreSuf():

    return getPreSuf("html_tags")


# Remove the delimiter
def getHtmlTags():

    os.chdir(dir)

    file = open("html_tags")
    contents = []

    for line in file:
        if line != "---":
            contents.append(line.replace("\n", ""))

    return contents

def getSqlKeywordsPreSuf():

    return getKeywordsContains("sql_keywords")


def getSqlKeywords():

    os.chdir(dir)

    file = open("sql_keywords")
    contents = []

    for line in file:
        if line != "---":
            contents.append(line.replace("\n", ""))

    return contents

def getSqlReservedWordsPreSuf():

    return getKeywordsContains("sql_reserved_words")

def getSqlReservedWords():

    os.chdir(dir)

    file = open("sql_reserved_words")
    contents = []

    for line in file:
        if line != "---":
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