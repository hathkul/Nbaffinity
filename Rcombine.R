# Set the working directory to the folder containing the CSV files
setwd("/Users/stepanchumakov/Nextcloud/Laboratory/AlphaFold/RFAntibody/RFab17032025/rf2output")  # Change this to your folder's path

# List all CSV files in the directory
files <- list.files(pattern = "\\.csv$")

# Process each file: read the file, extract the row of values (skipping the header),
# and add a new column for the file name.
all_data <- do.call(rbind, lapply(files, function(f) {
  # Read the file assuming the first row is header and the second row holds values
  d <- read.csv(f, header = TRUE, stringsAsFactors = FALSE)
  # d should now have one row (the values row)
  
  # Add a new column "file" containing the file name
  d_with_file <- cbind(file = f, d)
  return(d_with_file)
}))

# Write the combined data to a new CSV file without headers or row names.
write.table(all_data, file = "combined.csv", sep = ",", row.names = FALSE, col.names = FALSE, quote = FALSE)
