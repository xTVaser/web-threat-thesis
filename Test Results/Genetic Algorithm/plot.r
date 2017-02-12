# Recursively go through the directory given in order to plot the results on a graph.

# Testing set is 5000 large
# 30% for each attack and 10% normal so.
# 1500 SQL
# 1500 XSS
# 1500 RFI
# 500 Non threats (potential false positives)

generateGraph <- function(file, title, xLabel, yLabel) {

	# Variable
	table <- read.table(file, sep = "\t")

	png(filename=gsub(".dat", ".png", file), bg="white")

	x_min <- min(table[,1])
	x_max <- max(table[,1])
	plot(table[,1], table[,2], type="o", col="green", axes=FALSE, ann=FALSE, ylim=c(0, 100), xlim=c(x_min, x_max))

	box()
	grid(col="black")

	axis(1)
	axis(2, las=1)

	lines(table[,1], table[,3], type="o", pch=22, lty=1, col="red")
	lines(table[,1], table[,4], type="o", pch=22, lty=1, col="blue")

	title(main=title) # Variable
	title(xlab=xLabel) # Variable
	title(ylab=yLabel)

}

plotHelper <- function(directory, title, xLabel, yLabel) {

	files <- list.files(path = directory, pattern = "*.dat", recursive = TRUE, full.names = TRUE)
	for(file in files) {

		generateGraph(file, title, xLabel, yLabel)
	}
}

# Define Graph Structures Below
plotHelper("Determine Best Settings/Population Size", "SQL Population Size Effects", "Population Size (Individuals)", "Percentage (%)")
