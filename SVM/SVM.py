import argparse
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.font_manager
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from CommonLib.SVMRequest import getTrainingSet
from CommonLib.SVMRequest import getTestingSet

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--sqlNumber",
                    help="The number of SQL attacks to include in training")
parser.add_argument("-x", "--xssNumber",
                    help="The number of XSS attacks to include in training")
parser.add_argument("-r", "--rfiNumber",
                    help="The number of RFI attacks to include in training")
parser.add_argument("-n", "--ntNumber",
                    help="THe number of nonthreat attacks to include in training")

parser.add_argument("-f", "--fileDirectory",
                    help="Directory containing the 4 threat files for training")
parser.add_argument("-o", "--output",
                    help="Output file name")

args = parser.parse_args()

numSQL = int(args.sqlNumber)
numXSS = int(args.xssNumber)
numRFI = int(args.rfiNumber)
numNT = int(args.ntNumber)

directory = args.fileDirectory

sqlTestResults = []
xssTestResults = []
rfiTestResults = []

optimizedParameters = dict()

# Does a simple gridsearch to optimize gamma and C for the given kernel
def optimizeSVM(vectors, targets, kernel):

    accuracyResults = None
    precisionResults = None
    recallResults = None

    parameters = {'gamma': [0.1, 0.01, 0.001, 0.0001], 'C': [0.1, 1, 10, 100]}

    accuracyTest = GridSearchCV(svm.SVC(kernel=kernel), parameters, scoring="accuracy")
    accuracyTest.fit(vectors, targets)
    accuracyResults = accuracyTest.best_params_

    precisionTest = GridSearchCV(svm.SVC(kernel=kernel), parameters, scoring="precision")
    precisionTest.fit(vectors, targets)
    precisionResults = precisionTest.best_params_

    recallTest = GridSearchCV(svm.SVC(kernel=kernel), parameters, scoring="recall")
    recallTest.fit(vectors, targets)
    recallResults = recallTest.best_params_

    # Average of (gamma, C)
    averageGamma = (accuracyResults['gamma'] + precisionResults['gamma'] + recallResults['gamma']) / 3
    averageC = (accuracyResults['C'] + precisionResults['C'] + recallResults['C']) / 3

    optimizedParameters[kernel] = (averageGamma, averageC)


for t in range(3):

    figure = 1

    # Get all of the requests that we need from the files
    # The number of each, the type that we are trying to identify.
    # Will return a pair of two elements, the first being the requests and x,y positions, and the second being the targets 0 or 1
    testing = getTestingSet((t + 1), "Testing Data/")
    training = None

    if figure > 1: # We have finished the linear graph so we need to remove duplicates for complexity vs accuracy reasons
        training = getTrainingSet(numSQL, numXSS, numRFI, numNT, (t + 1), directory, True)
    else:
        training = getTrainingSet(numSQL, numXSS, numRFI, numNT, (t + 1), directory, False)

    # Take the response and convert it into a numpy array to be used by the SVM
    vectors = np.c_[training[0]]
    targets = training[1]

    # For now we will test with just linear
    for kernel in ('linear', 'poly', 'rbf'):

        # Need to optimize the kernel
        if kernel not in optimizedParameters:
            optimizeSVM(vectors, targets, kernel)

        # Create the SVM and setup its kernel and gamma and C values.
        # C = penality parameter of the error term
        # Gamma is the kernel coefficient for poly and rbf kernels
        # random_state can be used with a seed to shuffle the data, could be useful for averaging if decided to do so
        clf = svm.SVC(kernel=kernel,
                      gamma=optimizedParameters[kernel][0],
                      C=optimizedParameters[kernel][1],
                      cache_size=50000,
                      random_state=int(time.time()))

        # Train the classifier using the training vectors
        clf.fit(vectors, targets)

        # Begin the Plot
        plt.figure(figure, figsize=(10, 10))
        plt.clf()

        # Find max and min values to be used and scale it up a bit to give some margin space
        plt.axis('tight')
        x_min = -1
        x_max = max(vectors[:, 0]) + max(vectors[:, 0]) * 0.125
        y_min = -1
        y_max = max(vectors[:, 1]) + max(vectors[:, 1]) * 0.500

        # Set up the points
        s = 80
        # The points that lie nearest and determine the hard margins of the hyperplane
        support_vectors = plt.scatter(clf.support_vectors_[:, 0],
                                      clf.support_vectors_[:, 1],
                                      c = "yellow",
                                      zorder = 30,
                                      s = s / 2)

        attacks = []
        notattacks = []
        index = 0

        for pair in vectors:
            if(targets[index] == 1):
                attacks.append(pair)
            else:
                notattacks.append(pair)
            index += 1

        attacks = np.c_[attacks]
        notattacks = np.c_[notattacks]

        training_vectors_attacks = plt.scatter(attacks[:, 0], attacks[:, 1],
                                               c = "lightgreen",
                                               s = s,
                                               zorder = 10)
        training_vectors_nonattacks = plt.scatter(notattacks[:, 0], notattacks[:, 1],
                                                  c = "red",
                                                  s = s,
                                                  zorder = 20)

        # The decision function gives us the distance from the samples to the seperating hyperplane
        XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
        Z = clf.decision_function(np.c_[XX.ravel(), YY.ravel()])
        Z = Z.reshape(XX.shape)

        # Make the color backgrounds for the different areas
        plt.pcolormesh(XX, YY, Z > 0, cmap="copper")
        # Plot the dividing hyperplane and the buffer regions
        c = plt.contour(XX, YY, Z,
                        colors=['gray', 'black', 'gray'],
                        linestyles=['--', '-', '--'], linewidths=2,
                        levels=[-.5, 0, .5]) # full width of the regions

        # Simple legend
        plt.legend([support_vectors, training_vectors_attacks, training_vectors_nonattacks],
                   ["Support Vectors", "Attacks (Training)", "Non Attacks (Training)"],
                   prop=matplotlib.font_manager.FontProperties(size=16))

        # Axis definitions
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.xticks(())
        plt.yticks(())

        # Save the figure as a PNG file
        if t is 0:
            plt.title(args.output + " " + kernel.capitalize() + " SQL")
            plt.figure(figure).savefig("Results/" + args.output + " " + kernel.capitalize() + " SQL.png")
        elif t is 1:
            plt.title(args.output + " " + kernel.capitalize() + " XSS")
            plt.figure(figure).savefig("Results/" + args.output + " " + kernel.capitalize() + " XSS.png")
        elif t is 2:
            plt.title(args.output + " " + kernel.capitalize() + " RFI")
            plt.figure(figure).savefig("Results/" + args.output + " " + kernel.capitalize() + " RFI.png")

        figure += 1

        successfulDetections = 0
        falsePositives = 0
        incorrectDetections = 0

        # Get Test Results
        for info, type in zip(testing[0], testing[1]):

            x = info[0]
            y = info[1]
            testResult = clf.predict(np.c_[(x,y)])

            # Successful Detection
            if testResult[0] == 1 and type == (t + 1):
                successfulDetections += 1
            # False Positive
            elif testResult[0] == 1 and type == 0:
                falsePositives += 1
            # Incorrect Detection
            elif testResult[0] == 1 and type != (t + 1):
                incorrectDetections += 1

        successfulDetections = (successfulDetections / 1500.0) * 100.0
        falsePositives = (falsePositives / 500.0) * 100.0
        incorrectDetections = (incorrectDetections / 3000.0) * 100.0

        shortCodeKernel = ""
        if kernel is "linear":
            shortCodeKernel = "L"
        elif kernel is "poly":
            shortCodeKernel = "P"
        else:
            shortCodeKernel = "R"

        if t is 0:
            sqlTestResults.append((shortCodeKernel, successfulDetections, falsePositives, incorrectDetections))
        elif t is 1:
            xssTestResults.append((shortCodeKernel, successfulDetections, falsePositives, incorrectDetections))
        elif t is 2:
            rfiTestResults.append((shortCodeKernel, successfulDetections, falsePositives, incorrectDetections))


# Print to File
sqlFile = open("Results/SQL.res", "w+")
xssFile = open("Results/XSS.res", "w+")
rfiFile = open("Results/RFI.res", "w+")

for result in sqlTestResults:
    sqlFile.write(str(result[0]) + "\t" + str(result[1]) + "\t" + str(result[2]) + "\t" + str(result[3]) + "\n")
for result in xssTestResults:
    xssFile.write(str(result[0]) + "\t" + str(result[1]) + "\t" + str(result[2]) + "\t" + str(result[3]) + "\n")
for result in rfiTestResults:
    rfiFile.write(str(result[0]) + "\t" + str(result[1]) + "\t" + str(result[2]) + "\t" + str(result[3]) + "\n")

sqlFile.close()
xssFile.close()
rfiFile.close()
