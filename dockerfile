FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# -----------------------------
# SYSTEM DEPENDENCIES
# -----------------------------
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    r-base \
    default-jre \
    wget \
    git \
    build-essential \
    bowtie2 \
    samtools \
    fastqc \
    && apt-get clean

# -----------------------------
# R PACKAGES
# -----------------------------
RUN R -e "install.packages('BiocManager', repos='http://cran.r-project.org')" && \
    R -e "BiocManager::install('edgeR')" && \
    R -e "install.packages('pheatmap', repos='http://cran.r-project.org')"

# -----------------------------
# WORKDIR
# -----------------------------
WORKDIR /app

# -----------------------------
# COPY PROJECT
# -----------------------------
COPY . /app

# -----------------------------
# INSTALL PYTHON PACKAGE
# -----------------------------
RUN pip3 install --upgrade pip && \
    pip3 install -e .

# -----------------------------
# ENTRYPOINT
# -----------------------------
ENTRYPOINT ["pranomics"]
CMD ["run"]
