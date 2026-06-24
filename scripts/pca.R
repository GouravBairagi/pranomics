library(edgeR)
library(ggplot2)

args <- commandArgs(trailingOnly = TRUE)

count_file <- args[1]
meta_file  <- args[2]
out_file   <- args[3]

# -----------------------------
# Load data safely
# -----------------------------
counts <- read.csv(count_file, row.names = 1, check.names = FALSE)
meta <- read.csv(meta_file)

# Ensure sample match
common <- intersect(colnames(counts), meta$sample)

if (length(common) < 2) {
  stop("Not enough matching samples between counts and metadata")
}

counts <- counts[, common]
meta <- meta[match(common, meta$sample), ]

# -----------------------------
# Normalize
# -----------------------------
y <- DGEList(counts)
y <- calcNormFactors(y)
logCPM <- cpm(y, log = TRUE)

# -----------------------------
# PCA
# -----------------------------
pca <- prcomp(t(logCPM))

df <- data.frame(
  PC1 = pca$x[,1],
  PC2 = pca$x[,2],
  group = meta$group
)

png(out_file, width = 1200, height = 900)

ggplot(df, aes(PC1, PC2, color = group)) +
  geom_point(size = 3) +
  theme_minimal() +
  ggtitle("PCA Plot")

dev.off()
