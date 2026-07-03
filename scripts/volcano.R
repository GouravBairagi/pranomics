args <- commandArgs(trailingOnly = TRUE)

deg_file <- args[1]
out_file <- args[2]

deg <- read.csv(
  deg_file,
  row.names = 1,
  check.names = FALSE
)

# -----------------------------
# SAFE COLUMN HANDLING
# -----------------------------
if (!("FDR" %in% colnames(deg))) {
  if ("padj" %in% colnames(deg)) {
    deg$FDR <- deg$padj
  } else {
    stop("No FDR or padj column found in DEG file")
  }
}

if (!("logFC" %in% colnames(deg))) {
  if ("log2FoldChange" %in% colnames(deg)) {
    deg$logFC <- deg$log2FoldChange
  } else {
    stop("No logFC column found in DEG file")
  }
}

# -----------------------------
# CLEAN DATA
# -----------------------------
deg$FDR[is.na(deg$FDR)] <- 1
deg$logFC[is.na(deg$logFC)] <- 0

deg$Significant <- "Not Significant"

deg$Significant[
  deg$FDR < 0.05 &
  deg$logFC > 1
] <- "Upregulated"

deg$Significant[
  deg$FDR < 0.05 &
  deg$logFC < -1
] <- "Downregulated"

# -----------------------------
# PLOT
# -----------------------------
png(
  out_file,
  width = 1200,
  height = 900
)

plot(
  deg$logFC,
  -log10(deg$FDR + 1e-300),
  pch = 20,
  col = ifelse(
    deg$Significant == "Upregulated",
    "red",
    ifelse(
      deg$Significant == "Downregulated",
      "blue",
      "grey"
    )
  ),
  xlab = "log2 Fold Change",
  ylab = "-log10(FDR)",
  main = "Volcano Plot"
)

abline(v = c(-1, 1), lty = 2)
abline(h = -log10(0.05), lty = 2)

dev.off()
