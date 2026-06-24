library(edgeR)
library(pheatmap)

args <- commandArgs(trailingOnly = TRUE)

count_file <- args[1]
meta_file  <- args[2]
out_file   <- args[3]

counts <- read.csv(count_file, row.names = 1, check.names = FALSE)
meta <- read.csv(meta_file)

# Match samples safely
common <- intersect(colnames(counts), meta$sample)
counts <- counts[, common]
meta <- meta[match(common, meta$sample), ]

# Normalize
y <- DGEList(counts)
y <- calcNormFactors(y)
logCPM <- cpm(y, log = TRUE)

# Top variable genes
vars <- apply(logCPM, 1, var)
top_genes <- names(sort(vars, decreasing = TRUE))[1:50]

mat <- logCPM[top_genes, ]

annotation <- data.frame(group = meta$group)
rownames(annotation) <- meta$sample

png(out_file, width = 1200, height = 900)

pheatmap(
  mat,
  scale = "row",
  annotation_col = annotation,
  show_rownames = FALSE
)

dev.off()
