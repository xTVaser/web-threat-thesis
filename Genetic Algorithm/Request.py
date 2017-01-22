class Request(object):
    request = ""
    sql_decimal = ""
    sql_bitstrings = []
    xss_decimal = ""
    xss_bitstrings = []
    rfi_decimal = ""
    rfi_bitstrings = []
    attackType = 0

    def __init__(self, request, sql, xss, rfi):
        header = request.split()
        self.attackType = header[0]
        self.request = header[1]

        self.sql_bitstrings = addBitstrings(sql.split())
        self.xss_bitstrings = addBitstrings(xss.split())
        self.rfi_bitstrings = addBitstrings(rfi.split())

        self.sql_decimal = self.sql_bitstrings.pop(0)
        self.xss_decimal = self.xss_bitstrings.pop(0)
        self.rfi_decimal = self.rfi_bitstrings.pop(0)

    def __str__(self):

        if self.attackType is 0:
            return "Non-Attack: " + self.request
        elif self.attackType is 1:
            return "SQL Attack: " + self.sql_decimal + " - " + self.request
        elif self.attackType is 2:
            return "XSS Attack: " + self.xss_decimal + " - " + self.request
        else:
            return "RFI Attack: " + self.rfi_decimal + " - " + self.request



def addBitstrings(bitstrings):

    temp = []

    for i in range(len(bitstrings)):

        temp.append(bitstrings[i].split("."))

    return temp