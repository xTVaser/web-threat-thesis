# Recursively go through the directory given in order to plot the results on a graph.

# Testing set is 5000 large
# 30% for each attack and 10% normal so.
# 1500 SQL
# 1500 XSS
# 1500 RFI
# 500 Non threats (potential false positives)

generateLineGraph <- function(file, title, xLabel, yLabel) {

	# Variable
	table <- read.table(file, sep = "\t")
	table <- aggregate(. ~ V1, data=table, FUN=mean)

	print(table)
}

lineHelper <- function(directory, title, xLabel, yLabel) {

	files <- list.files(path = directory, pattern = "*.dat", recursive = TRUE, full.names = TRUE)
	for(file in files) {

		if(length(i <- grep("SQL", file))) {
			print(paste("SQL", title, sep=""))
			generateLineGraph(file, paste("SQL ", title, sep=""), xLabel, yLabel)
		}
		if(length(i <- grep("XSS", file))) {
			print(paste("XSS", title, sep=""))
			generateLineGraph(file, paste("XSS ", title, sep=""), xLabel, yLabel)
		}
		if(length(i <- grep("RFI", file))) {
			print(paste("RFI", title, sep=""))
			generateLineGraph(file, paste("RFI ", title, sep=""), xLabel, yLabel)
		}
	}
}

lineHelper("../SVM/Fair to Genetic", "Using Genetic Algorithm Training Set Scheme", "Training Distribution (SQL/XSS/RFI_Non Threat)", "Percentage (%)")
# Increasing Non-Threats (Should decrease False Positives)
lineHelper("../SVM/Increasing Non-Threats", "Increasing Only Non Threats with 300 Requests of XSS/SQL/RFI", "Amount of Non Threats in Training", "Percentage (%)")
# Increasing Incorrect Threats (Should decrease incorrect detections)
lineHelper("../SVM/Increasing Incorrect-Threats", "Constant Amount of Respective Request Type (300), Variable Other Two - Sorted by Incorrect Detection Rate", "Amonut of Variable Request Types", "Percentage (%)")


# Define Graph Structures Below
# Population Size
lineHelper("Determine Best Settings/Population Size", "Population Size Effect", "Population Size (Individuals)", "Percentage (%)")
# Mutation Rate
lineHelper("Determine Best Settings/Mutation Rate", "Mutation Rate Effect", "Mutation Rate (Percentage)", "Percentage (%)")
# Generation
lineHelper("Determine Best Settings/Generations", "Generations Effect", "Generations", "Percentage (%)")
# Elitist Pool
lineHelper("Determine Best Settings/Elitist Pool", "Elitist Pool Effect", "Elitist Pool (Percentage)", "Percentage (%)")
# Multiple Iterations
lineHelper("Multiple Iterations", "Multiple Iteration Effect", "Iterations", "Percentage (%)")
# Bitstring Length - Success Rate
lineHelper("Bitstring Length", "Bitstring Length Comparison", "Segment Lengths", "Percentage (%)")
