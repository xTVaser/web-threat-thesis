

# Commandline Arguments


# Training

# First read in all of the data from the parsed test files into some form of object structure
# These objects will contain the header information for the requests (what the request was and what type it truly is)
# They will also contain all of the bitstrings that the request may be interpreted as (sql/xss/rfi)

# Depending on the flag that tells us what attack type we are looking for, collect the respective bitstrings into a 2D array,
# Along with if they are attacks or not.

# Takes a certain % of the file usually 30% and trains with it, evolves and creates new bitstrings.
# This training set will go into a new list, but we test for fitness on the ENTIRE collection

# Evaluate all of the bitstrings using the genetic algorithm, and create new and delete unneeded ones based on fitness.


# Continue this until a stopping condition, such as a detection % is reached, or number of iterations is reached, or pop size, etc.

# Now training is complete, and our training array or list should contain a bunch of highly accurate bitstrings for detection.


# Testing

# Now we will use unseen data from a much larger collection

# Read the data into similar structures used in training
# Collect the relevant matching bitstrings

# If the same bitstrings match, then its a match, or a false positive.
# Use the header information to figure it out, all itstrings in our training array are attack signatures)

# Log all incidents and statistics to a file or array for later use.


# Output
# Output to a file with the top of the file having a summary of all of the information, and the details of the test