

df <- read.csv("C:/Courses/Ongoing/CS 748 - Advances In Intelligent and Learning Agents/Project - Scrabble Learner/code/scrabbler/agents/MoveTestingResults.csv",
               head = F, as.is=T,
               col.names = c("id", "moveno", "tilesinbag", "blankinrack", "gcgloc","gcgword","gcgscore",
                             "quackleloc","quackleword","quacklescore","greedyloc","greedyword","greedyscore")
)

df$quacklescore[is.na(df$quacklescore)] <- 0

df$QGsame <- (df$quackleloc == df$greedyloc) & (df$quackleword == df$greedyword)
df$QGequalscore <- (df$quacklescore == df$greedyscore)

nrow(df)
sum(df$QGsame)/nrow(df)
sum(df$QGequalscore)/nrow(df)



