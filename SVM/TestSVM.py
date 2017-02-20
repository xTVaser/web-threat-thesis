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

def incorrectTestHelper(variableNum):

    runTest(str(1000) + "_" + str(variableNum), "Increasing Incorrect-Threats/",
            1000, variableNum, variableNum, 350, "Training/New/", str(1000) + "_" + str(variableNum))

    runTest(str(1000) + "_" + str(variableNum), "Increasing Incorrect-Threats/",
            variableNum, 1000, variableNum, 350, "Training/New/", str(1000) + "_" + str(variableNum))

    runTest(str(1000) + "_" + str(variableNum), "Increasing Incorrect-Threats/",
            variableNum, variableNum, 1000, 350, "Training/New/", str(1000) + "_" + str(variableNum))


# Defined Tests Below
# Fair Comparisons using the same ratios as the genetic algorithm testing (30/30/30/10)
for i in range(3):

    runTest("75_25", "Fair to Genetic/", 75, 75, 75, 25, "Training/Old/", "75_25")
    # runTest("150_50", "Fair to Genetic/", 150, 150, 150, 50, "Training/Old/", "150_50")
    # runTest("300_100", "Fair to Genetic/", 300, 300, 300, 100, "Training/Old/", "300_100")
    # runTest("420_140", "Fair to Genetic/", 420, 420, 420, 420, "Training/Old/", "420_140")
    # runTest("562_189", "Fair to Genetic/", 562, 562, 562, 189, "Training/Old/", "562_189")
    # runTest("750_250", "Fair to Genetic/", 750, 750, 750, 250, "Training/Old/", "750_250")
    # runTest("1000_334", "Fair to Genetic/", 1000, 1000, 1000, 334, "Training/Old", "1000_334")
#
# # Increasing amounts of non-threat traiing (in theory should reduce false positives)
# runTest("350", "Increasing Non-Threats/", 1000, 1000, 1000, 350, "Training/New/", "350")
# runTest("450", "Increasing Non-Threats/", 1000, 1000, 1000, 450, "Training/New/", "450")
# runTest("550", "Increasing Non-Threats/", 1000, 1000, 1000, 550, "Training/New/", "550")
# runTest("700", "Increasing Non-Threats/", 1000, 1000, 1000, 700, "Training/New/", "700")
# runTest("1400", "Increasing Non-Threats/", 1000, 1000, 1000, 1400, "Training/New/", "1400")
# runTest("2000", "Increasing Non-Threats/", 1000, 1000, 1000, 2000, "Training/New/", "2000")
# runTest("2500", "Increasing Non-Threats/", 1000, 1000, 1000, 2500, "Training/New/", "2500")
#
# # Increasing amount of other attacks
# incorrectTestHelper(100)
# incorrectTestHelper(250)
# incorrectTestHelper(375)
# incorrectTestHelper(550)
# incorrectTestHelper(700)
# incorrectTestHelper(850)
# incorrectTestHelper(1000)
