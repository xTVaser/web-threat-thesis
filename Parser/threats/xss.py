import re
from CommonLib import decodeURL
from dictionaries.getDictionaries import getHtmlTagsPreSuf, getHtmlTags, getDOM, getDOMEventListeners, getDOMAttributes

# First Segment - Number of HTML/Script Keywords
# Second Segment - Encoded Character?
# Third Segment - Number of Fields with an XSS keyword
# Fourth Segment -  Attack Type
# Attack types are either - Reflected, Stored, DOM-Based
# 1 Reflected XSS - Displayed in some sort of alert or feedback, not persistent
# 2 DOM-Based - Similar to a stored or reflected attack, but typically involves the use of the DOM (document) object for javascript.
# 0 Attack that does not fit any of the criteria
# Stored XSS - Gets permanently stored on the target server cannot be determined as we have no context on how the data will be treated
def xssBitstring(request, isSVM):

    workingRequest = decodeURL(request)

    segments = []

    simpleTags = getHtmlTags()
    preSufTags = getHtmlTagsPreSuf()

    totalKeywords = 0

    for line in preSufTags:

        tags = line.split(" ")
        uniqueTags = 0

        tagCount = workingRequest.lower().count(tags[0])

        if tagCount > 0 and len(tags) > 1:

            # Used to be -2 but that was a problem in sql so changed here as well
            for x in range(len(tags) - 1):

                uniqueTags += workingRequest.lower().count(tags[x+1])

        tagCount -= uniqueTags
        totalKeywords += tagCount

    segments.append(totalKeywords)

    if isSVM is False:
        # See if encoded or not
        if request != workingRequest:
            segments.append(1)
        else:
            segments.append(0)

    # Regex to match with all fields
    fields = re.compile("(\?|&)[\w\d]+=").split(workingRequest)
    del fields[1::2]  # Get rid of every second element because the regex is fine but python adds non-existant characters?
    del fields[0]  # Delete the first field because it isnt a field

    numFieldsWithKeyword = 0

    for field in fields:

        for tag in simpleTags:

            if tag.lower() in field.lower():
                numFieldsWithKeyword += 1
                break

    segments.append(numFieldsWithKeyword)

    if isSVM is False:
        # ATTACK TYPES
        # Reflected XSS - Not persistent, displayed in some sort of feedback to the user
        windowObject = ["alert", "close", "confirm", "moveBy", "moveTo",
                        "open", "prompt", "resizeBy", "resizeTo", "scrollBy",
                        "scrollTo", "scroll"]
        historyObject = ["back", "forward", "go", "assign", "reload", "replace"]
        locationObject = ["hash", "host", "hostname", "href", "pathname", "port", "protocol", "search"]

        reflectedFlag = False

        for method in windowObject:

            if method in workingRequest.lower() or "window." + method in workingRequest.lower():
                reflectedFlag = True
                break

        for method in historyObject:

            if "history." + method in workingRequest.lower():
                reflectedFlag = True
                break

        for method in locationObject:

            if "location." + method in workingRequest.lower():
                reflectedFlag = True
                break

        if reflectedFlag is True:
            segments.append(1)

        # DOM XSS - Manipulating the DOM Object in someway.
        # An attack could fall under many categories, but in this case we are considering reflected as the priority

        domMethods = getDOM()                           # These methods all have to start with document.<...>
        domEventListeners = getDOMEventListeners()      # These event listeners don't, they are just attributes of tags
        domAttributes = getDOMAttributes()

        domXSSFlag = False

        for method in domMethods:

            if "document." + method in workingRequest.lower():
                domXSSFlag = True
                break

        for listener in domEventListeners:

            if listener in workingRequest.lower():
                domXSSFlag = True
                break

        for attribute in domAttributes:

            numAttributes = re.compile("<.*"+attribute+".*>").findall(workingRequest.lower())

            if len(numAttributes) > 0:
                domXSSFlag = True
                break

        if domXSSFlag is True and reflectedFlag is False:
            segments.append(2)
        elif domXSSFlag is False and reflectedFlag is False:    # Didnt match either.
            segments.append(0)

    return segments