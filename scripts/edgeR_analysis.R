library(edgeR)

args <- commandArgs(trailingOnly=TRUE)

count_file <- args[1]
meta_file <- args[2]
output_file <- args[3]

counts <- read.csv(
  count_file,
  row.names=1,
  check.names=FALSE
)

meta <- read.csv(meta_file)

counts <- counts[, meta$sample]

group <- factor(meta$group)

y <- DGEList(
  counts=counts,
  group=group
)

keep <- filterByExpr(y)

y <- y[keep,,keep.lib.sizes=FALSE]

y <- calcNormFactors(y)

design <- model.matrix(~group)

y <- estimateDisp(y, design)

fit <- glmQLFit(y, design)

qlf <- glmQLFTest(fit)

res <- topTags(
  qlf,
  n=Inf
)$table

write.csv(
  res,
  output_file
)
