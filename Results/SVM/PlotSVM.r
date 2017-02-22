# Recursively go through the directory given in order to plot the results on a graph.

# Testing set is 5000 large
# 30% for each attack and 10% normal so.
# 1500 SQL
# 1500 XSS
# 1500 RFI
# 500 Non threats (potential false positives)

generateGroupedBarChart <- function(file, title, xLabel, yLabel, sortColumn, sortOrder) {

	# Variable
	table <- read.table(file, sep = "\t")
	table <- aggregate(. ~ V1, data=table, FUN=mean)
	table <- table[ order(table[,sortColumn], decreasing=sortOrder), ]
	subset <- t(data.frame(table[,2], table[,3], table[,4]))

	filename <- gsub(".dat", ".png", file)

	png(filename=filename, width=1000, units="px", bg="white")

	op <- par(mar = c(9,5,4,2) + 0.1)

	barplot(subset, names.arg=table[,1], col=c("#21d106", "#d10606", "#ebef04"), legend=c("Successful", "False Positive", "Incorrect"), ylim=c(0,120), beside=TRUE, las=2)

	box()

	title(main=title) # Variable
	title(xlab=xLabel, font.lab=2, line=7) # X Axis
	title(ylab=yLabel, font.lab=2)

	par(op)
}

barHelper <- function(directory, title, xLabel, yLabel, sortColumn, sortOrder) {

	files <- list.files(path = directory, pattern = "*.dat", recursive = TRUE, full.names = TRUE)
	for(file in files) {

		if(length(i <- grep("SQL", file)))
			generateGroupedBarChart(file, paste("SQL - ", title, sep=""), xLabel, yLabel, sortColumn, sortOrder)
		if(length(i <- grep("XSS", file)))
			generateGroupedBarChart(file, paste("XSS - ", title, sep=""), xLabel, yLabel, sortColumn, sortOrder)
		if(length(i <- grep("RFI", file)))
			generateGroupedBarChart(file, paste("RFI - ", title, sep=""), xLabel, yLabel, sortColumn, sortOrder)
	}
}


# Define Graph Structures Below
# Fair to Genetic Algorithm Comparison
barHelper("Fair to Genetic", "Using Genetic Algorithm Training Set Scheme - Sorted by Success Rate", "Training Distribution (SQL/XSS/RFI_Non Threat)", "Percentage (%)", 2, TRUE)
# Increasing Non-Threats (Should decrease False Positives)
barHelper("Increasing Non-Threats", "Increasing Only Non Threats with 300 Requests of XSS/SQL/RFI - Sorted by False Positive Rate", "Amount of Non Threats in Training", "Percentage (%)", 3, TRUE)
# Increasing Incorrect Threats (Should decrease incorrect detections)
barHelper("Increasing Incorrect-Threats", "Constant Amount of Respective Request Type (300), Variable Other Two - Sorted by Incorrect Detection Rate", "Amonut of Variable Request Types", "Percentage (%)", 4, TRUE)
