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

	png(filename=gsub(".dat", ".png", file), bg="white")

	x_min <- min(table[,1])
	x_max <- max(table[,1])
	plot(table[,1], table[,2], type="o", col="#21d106", axes=FALSE, ann=FALSE, ylim=c(0, 123), xlim=c(x_min, x_max), lwd=4)

	box()
	grid(col="black")

	axis(1)
	axis(2, las=1)

	lines(table[,1], table[,3], type="o", pch=22, lty=1, col="#d10606", lwd=4)
	lines(table[,1], table[,4], type="o", pch=22, lty=1, col="#dddd08", lwd=4)

	title(main=title) # Variable
	title(xlab=xLabel) # Variable
	title(ylab=yLabel)

	legend(x_min+(x_max/500), 125, c("Successful", "False Positive", "Incorrect"), col=c("#21d106","#d10606", "#dddd08"), pch=21:22, lty=1);
}

lineHelper <- function(directory, title, xLabel, yLabel) {

	files <- list.files(path = directory, pattern = "*.dat", recursive = TRUE, full.names = TRUE)
	for(file in files) {

		if(length(i <- grep("SQL", file)))
			generateLineGraph(file, paste("SQL ", title, sep=""), xLabel, yLabel)
		if(length(i <- grep("XSS", file)))
			generateLineGraph(file, paste("XSS ", title, sep=""), xLabel, yLabel)
		if(length(i <- grep("RFI", file)))
			generateLineGraph(file, paste("RFI ", title, sep=""), xLabel, yLabel)
	}
}

generateGroupedBarChart <- function(file, title, subtitle, xLabel, yLabel, sortColumn) {

	# Variable
	table <- read.table(file, sep = "\t")
	table <- aggregate(. ~ V1, data=table, FUN=mean)
	table <- table[ order(table[,sortColumn], decreasing=TRUE), ]
	subset <- t(data.frame(table[,2], table[,3], table[,4]))

	filename <- gsub("Results", paste("Results_", subtitle, sep=""), file)
	filename <- gsub(".dat", ".png", filename)

	png(filename=filename, width=1000, units="px", bg="white")

	barplot(subset, names.arg=table[,1], col=c("#21d106", "#d10606", "#ebef04"), legend=c("Successful", "False Positive", "Incorrect"), ylim=c(0,120), beside=TRUE, las=2)

	box()

	title(main=paste(title, subtitle, sep="")) # Variable
	title(xlab=xLabel, font.lab=2) # Variable
	title(ylab=yLabel, font.lab=2)
}

barHelper <- function(directory, title, subtitle, xLabel, yLabel, sortColumn) {

	files <- list.files(path = directory, pattern = "*.dat", recursive = TRUE, full.names = TRUE)
	for(file in files) {

		if(length(i <- grep("SQL", file)))
			generateGroupedBarChart(file, paste("SQL ", title, sep=""), subtitle, xLabel, yLabel, sortColumn)
		if(length(i <- grep("XSS", file)))
			generateGroupedBarChart(file, paste("XSS ", title, sep=""), subtitle, xLabel, yLabel, sortColumn)
		if(length(i <- grep("RFI", file)))
			generateGroupedBarChart(file, paste("RFI ", title, sep=""), subtitle, xLabel, yLabel, sortColumn)
	}
}


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
barHelper("Bitstring Length", "Bitstring Length Comparison - Sorted by ", "Success Rate", "Segment Lengths", "Percentage (%)", 2)
# Bitstring Length - False Positives
barHelper("Bitstring Length", "Bitstring Length Comparison - Sorted by ", "False Positives", "Segment Lengths", "Percentage (%)", 3)
# Bitstring Length - Wrong Detection
barHelper("Bitstring Length", "Bitstring Length Comparison - Sorted by ", "Wrong Detections", "Segment Lengths", "Percentage (%)", 4)
