library(edgeR)
library(pheatmap)

args <- commandArgs(trailingOnly = TRUE)

count_file <- args[1]
meta_file  <- args[2]
out_file   <- args[3]

# -----------------------------
# LOAD DATA
# -----------------------------
counts <- read.csv(count_file, row.names = 1, check.names = FALSE)
meta <- read.csv(meta_file)

# -----------------------------
# MATCH SAMPLES SAFELY
# -----------------------------
common <- intersect(colnames(counts), meta$sample)

if (length(common) < 2) {
  stop("Not enough matching samples between counts and metadata")
}

counts <- counts[, common]
meta <- meta[match(common, meta$sample), ]

# -----------------------------
# DETECT GROUP COLUMN SAFELY
# -----------------------------
group_col <- NULL

if ("group" %in% colnames(meta)) {
  group_col <- meta$group
} else if ("condition" %in% colnames(meta)) {
  group_col <- meta$condition
} else if ("treatment" %in% colnames(meta)) {
  group_col <- meta$treatment
} else {
  stop("No grouping column found (expected: group/condition/treatment)")
}

# -----------------------------
# NORMALIZATION
# -----------------------------
y <- DGEList(counts)
y <- calcNormFactors(y)
logCPM <- cpm(y, log = TRUE)

# -----------------------------
# TOP VARIABLE GENES
# -----------------------------
vars <- apply(logCPM, 1, var)
top_genes <- names(sort(vars, decreasing = TRUE))[1:min(50, length(vars))]

mat <- logCPM[top_genes, , drop = FALSE]

# -----------------------------
# ANNOTATION
# -----------------------------
annotation <- data.frame(group = group_col)
rownames(annotation) <- meta$sample

# -----------------------------
# OUTPUT
# -----------------------------
png(out_file, width = 1200, height = 900)

pheatmap(
  mat,
  scale = "row",
  annotation_col = annotation,
  show_rownames = FALSE
)

dev.off()
