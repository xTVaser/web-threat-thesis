# Seperate our sample files into files with for example 500 sql, another 500 xss, etc. 250 normal requests.
# Use this file to combine them all into one test file that we can use.

# usage would be generateTest.py -xss <file with xss> -normal <file with non-attacks>...so on...-xssPer 25 -sqlPer 25,
# allows us to change the proportion of the test files as well for later on if that is needed.

# <request> <type> type is 0-4, 0 being a non threat, 1 being sql, 2 xss, 3 rfi attack.

