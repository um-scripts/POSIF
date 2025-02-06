library(DESeq2)
library(tidyverse)

counts_data <- read.csv('reads.csv', header = TRUE, row.names = 1)
colnames(counts_data)
head(counts_data)

sample_info <- read.csv('info.csv', header = TRUE, row.names = 1)
colnames(sample_info)
head(sample_info)

all(colnames(counts_data) %in% rownames(sample_info))
all(colnames(counts_data) == row.names(sample_info))


dds <-DESeqDataSetFromMatrix(countData = counts_data, 
                             colData = sample_info, 
                             design = ~ Stress)
dds <- estimateSizeFactors(dds)
#=================To save the normalized read counts===========================
#dds <- estimateSizeFactors(dds)
#sizeFactors(dds)
#normalized_counts <- counts(dds, normalized= TRUE)
#normalized_counts
#write.table(normalized_counts, file="normalized_counts.tsv", sep= "\t", quote=F, col.names = NA)
#============================================
dds

#SetFactorLevel
dds$Stress <- relevel(dds$Stress, ref = "untreated")


dds <- DESeq(dds)
res <- results(dds)
plotMA(res)

res0.05 <- results(dds, alpha = 0.05)
summary(res)
summary(res0.05)



