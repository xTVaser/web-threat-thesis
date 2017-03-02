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

	png(filename=gsub(".res", ".png", file), bg="white")

	x_min <- min(table[,1])
	x_max <- max(table[,1])
	plot(table[,1], table[,2], type="o", col="#21d106", axes=FALSE, ann=FALSE, ylim=c(0, 123), xlim=c(x_min, x_max), lwd=4)

	box()
	grid(col="black")

	axis(1)
	axis(2, las=1)

	lines(table[,1], table[,3], type="o", pch=22, lty=1, col="#d10606", lwd=7)
	lines(table[,1], table[,4], type="o", pch=22, lty=1, col="#dddd08", lwd=4)

	title(main=title) # Variable
	title(xlab=xLabel) # Variable
	title(ylab=yLabel)

	legend(x_min+(x_max/500), 125, c("Successful", "False Positive", "Incorrect"), col=c("#21d106","#d10606", "#dddd08"), pch=21:22, lty=1);
}

lineHelper <- function(directory, title, xLabel, yLabel) {

	files <- list.files(path = directory, pattern = "*.res", recursive = TRUE, full.names = TRUE)
	for(file in files) {

		if(length(i <- grep("SQL", file)))
			generateLineGraph(file, paste("SQL - ", title, sep=""), xLabel, yLabel)
		if(length(i <- grep("XSS", file)))
			generateLineGraph(file, paste("XSS - ", title, sep=""), xLabel, yLabel)
		if(length(i <- grep("RFI", file)))
			generateLineGraph(file, paste("RFI - ", title, sep=""), xLabel, yLabel)
	}
}

# Define Graph Structures Below
lineHelper("Random Permutations With Fitness", "Random Permutations", "Percentage of Permutated Signatures Used", "Percentage (%)")
