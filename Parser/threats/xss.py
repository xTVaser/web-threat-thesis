import os
import re
from urllib import parse

htmltags = open("../assets/htmltags.txt", "r").readlines()

attacks = open("../testing/Bitstrings/xss_Small", "r")
tempFile = open("../testing/Bitstrings/xss_Small.tmp", "w")

requests = attacks.readlines()

line = requests[0]
request = parse.unquote(line)

encodeFlag = False
tagCount = 0
fieldTagCount = 0

for request in requests:
    if request != parse.unquote(request):
        encodeFlag = True

    request = parse.unquote(request)

    # issue where tag like <b also matches a <body tag
    # can subtract these out later if i care to do so
    for tag in htmltags:
        if tag.replace("\n","") in request.lower():
            tagCount += 1

    fields = request.split("&")

    for field in fields:
        if "=" in field:
            for tag in htmltags:
                if tag.replace("\n", "") in field.lower():
                    fieldTagCount += 1

    # check if reflected XSS attack
    # check for alert, msgbox, etc.



    if tagCount > 7:
        tagCount = 7
    if fieldTagCount > 7:
        fieldTagCount = 7

    tempFile.write(request.replace("\n", "") + "\t" + bin(tagCount)[2:].zfill(3) + "" + str(int(encodeFlag)) + "" + bin(fieldTagCount)[2:].zfill(3) + "\n")
    tagCount = 0
    fieldTagCount = 0
    encodedFlag = False

