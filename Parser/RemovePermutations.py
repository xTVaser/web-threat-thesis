input = open("Parsed_Training_GA", "r")
output = open("Parsed_Training_GA_NoPermute", "w+")

num_lines = 5000

for i in range(num_lines):

    output.write(input.readline())
    sqlLine = input.readline().split()
    output.write(sqlLine[0] + " " + sqlLine[len(sqlLine)-1] + "\n")
    xssLine = input.readline().split()
    output.write(xssLine[0] + " " + xssLine[len(xssLine)-1] + "\n")
    rfiLine = input.readline().split()
    output.write(rfiLine[0] + " " + rfiLine[len(rfiLine)-1] + "\n")

output.close()