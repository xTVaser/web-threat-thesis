import os
import shutil
import sys
import time
from subprocess import DEVNULL, STDOUT, run

# Calling Syntax

# Setup Environment
print("Deleting Results Folder")
try:
    print("Deletion current disabled for testing reasons")
    # shutil.rmtree("Results/")
except:
    print("No Results Folder Found")

# os.mkdir("Results/")

def runTest(testName, outputFolder,
            numSQL, numXSS, numRFI, numNT, optimize,
            directory, outputFile):

    for t in range(3):

        print("")

        outputDir = "../Test Results/SVM/" + outputFolder + testName + "/"

        print("Running:\t" + testName + "\t\tWill be Stored In:\t" + outputDir)
        print("Arguments: # SQL: " + numSQL + ", # XSS: " + numXSS + ", # RFI: " + numRFI + ", # NT: " + numNT +
              ", Optimize: " + optimize)

        timeStart = time.time()

        cmd = ("python3 SVM.py -s " + numSQL + " -x " + numXSS + " -r " + numRFI + " -n " + numNT +
               + " -op " + optimize + " -f " + directory + " -o " + outputFile)

        sys.stdout.write("...")
        sys.stdout.flush()
        run(cmd.split(), stdout=DEVNULL, stderr=STDOUT)

        resultFiles = os.listdir("Results/")

        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

        for file in resultFiles:

            shutil.move("Results/" + file, outputDir + file)

        timeEnd = time.strftime("%M:%S", time.localtime(time.time() - timeStart))
        sys.stdout.write("Finished in " + str(timeEnd) + "\n")

def incorrectTestHelper(variableNum):

    runTest(str(1000) + "_" + str(variableNum), "Increasing Incorrect-Threats/",
            1000, variableNum, variableNum, 350, True, "Training Data/New Set", str(1000) + "_" + str(variableNum))

    runTest(str(1000) + "_" + str(variableNum), "Increasing Incorrect-Threats/",
            variableNum, 1000, variableNum, 350, True, "Training Data/New Set", str(1000) + "_" + str(variableNum))

    runTest(str(1000) + "_" + str(variableNum), "Increasing Incorrect-Threats/",
            variableNum, variableNum, 1000, 350, True, "Training Data/New Set", str(1000) + "_" + str(variableNum))


# Defined Tests Below
# Fair Comparisons using the same ratios as the genetic algorithm testing (30/30/30/10)
runTest("75_25", "Fair to Genetic/", 75, 75, 75, 25, True, "Training Data/Old Set", "75_25")
runTest("150_50", "Fair to Genetic/", 150, 150, 150, 50, True, "Training Data/Old Set", "150_50")
runTest("300_100", "Fair to Genetic/", 300, 300, 300, 100, True, "Training Data/Old Set", "300_100")
runTest("420_140", "Fair to Genetic/", 420, 420, 420, 420, True, "Training Data/Old Set", "420_140")
runTest("562_189", "Fair to Genetic/", 562, 562, 562, 189, True, "Training Data/Old Set", "562_189")
runTest("750_250", "Fair to Genetic/", 750, 750, 750, 250, True, "Training Data/Old Set", "750_250")
runTest("1000_334", "Fair to Genetic/", 1000, 1000, 1000, 334, True, "Training Data/Old Set", "1000_334")

# Increasing amounts of non-threat traiing (in theory should reduce false positives)
runTest("350", "Increasing Non-Threats/", 1000, 1000, 1000, 350, True, "Training Data/New Set", "350")
runTest("450", "Increasing Non-Threats/", 1000, 1000, 1000, 450, True, "Training Data/New Set", "450")
runTest("550", "Increasing Non-Threats/", 1000, 1000, 1000, 550, True, "Training Data/New Set", "550")
runTest("700", "Increasing Non-Threats/", 1000, 1000, 1000, 700, True, "Training Data/New Set", "700")
runTest("1400", "Increasing Non-Threats/", 1000, 1000, 1000, 1400, True, "Training Data/New Set", "1400")
runTest("2000", "Increasing Non-Threats/", 1000, 1000, 1000, 2000, True, "Training Data/New Set", "2000")
runTest("2500", "Increasing Non-Threats/", 1000, 1000, 1000, 2500, True, "Training Data/New Set", "2500")

# Increasing amount of other attacks
incorrectTestHelper(100)
incorrectTestHelper(250)
incorrectTestHelper(375)
incorrectTestHelper(550)
incorrectTestHelper(700)
incorrectTestHelper(850)
incorrectTestHelper(1000)
