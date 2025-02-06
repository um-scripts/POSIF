library(DESeq2)
library(tidyverse)

counts_data <- read.csv('reads.csv', header = TRUE, row.names = 1)
sample_info <- read.csv('info.csv', header = TRUE, row.names = 1)

stopifnot(identical(colnames(counts_data), rownames(sample_info)))

dds <- DESeqDataSetFromMatrix(countData = counts_data, 
                              colData = sample_info, 
                              design = ~ Stress)

dds$Stress <- relevel(dds$Stress, ref = "untreated")

dds <- DESeq(dds)

res <- results(dds)
res0.05 <- results(dds, alpha = 0.05)

normalized_counts <- counts(dds, normalized= TRUE)
write.table(normalized_counts, file="normalized_counts.tsv", sep= "\t", quote=F, col.names = NA)

write.csv(as.data.frame(res0.05), "DE_results.csv")

plotMA(res0.05)

summary(res)
summary(res0.05)
