import re
from CommonLib import decodeURL


def rfiBitstringSVM(request):
    print("ye")

# First Segment - Number of URLs
# Second Segment - Encoded or Not
# Third Segment - Number of Commands
# Fourth Segment -  Attack Type
# Attack Types are either URL, Command, or URL and Command
# A URL is just the presence of a URL
# A Command is one of the php reserved word commands, include() include_once(), etc, do not count.
def rfiBitstring(request, isSVM):
    # If we are finding for SVM, we will do things differently (may not even be a bitstring)
    if isSVM is True:
        return rfiBitstringSVM(request)

    workingRequest = decodeURL(request)

    # Else, go about solving the comments above

    segments = []

    # Num URLs
    numURLs = workingRequest.count("http://www")
    segments.append(numURLs)

    # Check if Encoded
    if request != workingRequest:
        segments.append(1)
    else:
        segments.append(0)

    # Check number of Commands

    numCMDs = 0

    phpCommands = ["__halt_compiler(",
                   "die(",
                   "empty(",
                   "list(",
                   "unset(",
                   "eval(",
                   "array(",
                   "exit(",
                   "isset("]

    for command in phpCommands:
        numCMDs += workingRequest.count(command)

    segments.append(numCMDs)

    # Finally, figure out the attack type.

    if numCMDs > 0 and numURLs > 0:
        segments.append(3)  #URL AND COMMAND
    elif numCMDs > 0:
        segments.append(2)  #COMMAND
    elif numURLs > 0:
        segments.append(1)  #URL
    else:
        segments.append(0)  #Fits no Attack Type, maybe still rfi

    return segments