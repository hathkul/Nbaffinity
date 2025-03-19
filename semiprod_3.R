load(".RData")
library(tidyverse)
library(caret)

args <- commandArgs(trailingOnly = TRUE)
if (length(args) == 0) {
  stop("No input file provided. Please specify a CSV file as an argument.")
}
# The first argument is your input file name
input_file <- args[1]

unknown <- read.csv(input_file,header = F) #Import your data; better without column name, if you have, please set "header = T".
protein_names <- unknown[[1]]
numeric_data <- unknown[,-1]
colnames(numeric_data) <- name  # 'name' is your vector of predictor names

unknownS <- predict(preprocessParams, numeric_data)

unknownprediction <- data.frame(name = protein_names, #the name of your protein, if you have.
                           preclass=predict(TdataSW.roF1,unknownS), #Give the class of affinity of the candidate nanobody
                           preprob=predict(TdataSW.roF1,unknownS,type = 'prob' )) #Give the probability of the class

# Create the output filename by replacing ".csv" with "_nbpred.csv"
output_file <- sub("\\.csv$", "_nbpred.csv", input_file)
# If the input file doesn't have a .csv extension, simply append "_nbpred.csv"
if (output_file == input_file) {
  output_file <- paste0(input_file, "_nbpred.csv")
}

# Write the output to the generated filename
write.csv(unknownprediction, output_file, row.names = FALSE)
