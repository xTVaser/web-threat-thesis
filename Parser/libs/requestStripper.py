def gatherStrings(array, file):
    for line in open(file):
        array.append(line)


def exportFile(lines, file):

    for l in lines:
        request = l.split("\"")[1]
        file.write(request+"\n")