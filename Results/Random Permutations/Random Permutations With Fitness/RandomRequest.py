class RandomRequest(object):

    request = ""
    sql = []
    xss = []
    rfi = []
    fitness = 0
    attackType = 0

    def __init__(self, request, sql, xss, rfi):
        header = request.split()
        self.attackType = header[0]
        self.request = header[1]

        self.sql = sql
        self.xss = xss
        self.rfi = rfi

    def setFitness(self, fitness):

        self.fitness = fitness

    def __str__(self):

        if self.attackType is "0":
            return "Non-Attack: " + self.request
        elif self.attackType is "1":
            return "SQL Attack: " + self.request
        elif self.attackType is "2":
            return "XSS Attack: " + self.request
        else:
            return "RFI Attack: " + self.request

