import os
import shutil
import sys
import time
from subprocess import DEVNULL, STDOUT, run

# Calling Syntax

# Setup Environment
print("Deleting Results Folder")
try:
    # print("Deletion current disabled for testing reasons")
    shutil.rmtree("Results/")
except:
    print("No Results Folder Found")

os.mkdir("Results/")

def runTest(testName, outputFolder,
            numSQL, numXSS, numRFI, numNT,
            directory, outputFile):

    print("")

    outputDir = "../Results/SVM/" + outputFolder + testName + "/"

    print("Running:\t" + testName + "\t\tWill be Stored In:\t" + outputDir)
    print("Arguments: # SQL: "
          + str(numSQL) + ", # XSS: "
          + str(numXSS) + ", # RFI: "
          + str(numRFI) + ", # NT: "
          + str(numNT))

    timeStart = time.time()

    cmd = ("python3 SVM.py -s " + str(numSQL) + " -x " + str(numXSS) + " -r " + str(numRFI) + " -n " + str(numNT) +
           " -f " + directory + " -o " + outputFile)

    sys.stdout.write("...")
    sys.stdout.flush()
    run(cmd.split(), stdout=DEVNULL, stderr=STDOUT)

    resultFiles = os.listdir("Results/")

    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    for file in resultFiles:

        if file.endswith(".res"):

            if file == "SQL.res":
                printResults("../Results/SVM/" + outputFolder + "Results_SQL.dat", open("Results/" + file).readlines(), testName)
            elif file == "XSS.res":
                printResults("../Results/SVM/" + outputFolder + "Results_XSS.dat", open("Results/" + file).readlines(), testName)
            else:
                printResults("../Results/SVM/" + outputFolder + "Results_RFI.dat", open("Results/" + file).readlines(), testName)

        elif file.endswith(".png"):

            # Move to a seperate folder
            shutil.move("Results/" + file, outputDir + file)


    timeEnd = time.strftime("%M:%S", time.localtime(time.time() - timeStart))
    sys.stdout.write("Finished in " + str(timeEnd) + "\n")

def printResults(file, lines, testName):

    currentFile = None

    if os.path.exists(file):
        currentFile = open(file, "a")
    else:
        currentFile = open(file, "w+")

    for line in lines:
        currentFile.write(testName + line)

    currentFile.close()

# Method has an issue that was fixed manually in the resulting files.
# It should only run each one for its respective type, not all 3 like the SVM automatically does
# As we are only interested in where the type is held constant and the incorrect changes.
def incorrectTestHelper(variableNum):

    # SQL Constant
    runTest(str(variableNum), "Increasing Incorrect-Threats/",
            300, variableNum, variableNum, 350, "Training/New/", str(300) + "_" + str(variableNum))

    # XSS Constant
    runTest(str(variableNum), "Increasing Incorrect-Threats/",
            variableNum, 300, variableNum, 350, "Training/New/", str(300) + "_" + str(variableNum))

    # RFI Constant
    runTest(str(variableNum), "Increasing Incorrect-Threats/",
            variableNum, variableNum, 300, 350, "Training/New/", str(300) + "_" + str(variableNum))


# Defined Tests Below
# Fair Comparisons using the same ratios as the genetic algorithm testing (30/30/30/10)
runTest("75_25", "Fair to Genetic/", 75, 75, 75, 25, "Training/New/", "75_25")
runTest("150_50", "Fair to Genetic/", 150, 150, 150, 50, "Training/New/", "150_50")
runTest("300_100", "Fair to Genetic/", 300, 300, 300, 100, "Training/New/", "300_100")
runTest("420_140", "Fair to Genetic/", 420, 420, 420, 140, "Training/New/", "420_140")
runTest("562_189", "Fair to Genetic/", 562, 562, 562, 189, "Training/New/", "562_189")
runTest("750_250", "Fair to Genetic/", 750, 750, 750, 250, "Training/New/", "750_250")
runTest("1000_334", "Fair to Genetic/", 1000, 1000, 1000, 334, "Training/New/", "1000_334")

# # Increasing amounts of non-threat training (in theory should reduce false positives)
runTest("50", "Increasing Non-Threats/", 300, 300, 300, 50, "Training/New/", "50")
runTest("100", "Increasing Non-Threats/", 300, 300, 300, 100, "Training/New/", "100")
runTest("200", "Increasing Non-Threats/", 300, 300, 300, 200, "Training/New/", "200")
runTest("350", "Increasing Non-Threats/", 300, 300, 300, 350, "Training/New/", "350")
runTest("500", "Increasing Non-Threats/", 300, 300, 300, 500, "Training/New/", "500")
runTest("750", "Increasing Non-Threats/", 300, 300, 300, 750, "Training/New/", "750")

# # Increasing amount of other attacks
incorrectTestHelper(50)
incorrectTestHelper(100)
incorrectTestHelper(200)
incorrectTestHelper(275)
incorrectTestHelper(350)
incorrectTestHelper(600)
incorrectTestHelper(750)