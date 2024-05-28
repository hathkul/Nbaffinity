R
load(".RData")
library(tidyverse)
library(caret)
unknown <- read.csv("yourfile.csv",header = F,col.names = name)
unknownS <- scale(unknown[,-1])
unknownprediction <- data.frame(name=unknown$name,
                                preclass=predict(TdataSW.roF1,unknownS),
                                preprob=predict(TdataSW.roF1,unknownS,type = 'prob' ))
write.csv(unknownprediction,'unknownprediction.csv')

