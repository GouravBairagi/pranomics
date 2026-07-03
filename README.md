# 🧬 Pranomics

**Pranomics** is a fully automated RNA-seq analysis pipeline that takes raw sequencing data (SRA/FASTQ) all the way to differential expression analysis and publication-ready reports — in a single command.

It integrates widely used bioinformatics tools like **FastQC, Bowtie2, Samtools, StringTie, and edgeR**, wrapped in an easy-to-use Python CLI.

---

# 🚀 Features

- 🔄 One-command RNA-seq pipeline
- 📥 Automatic SRA → FASTQ conversion
- 🔬 Quality control (FastQC)
- ✂️ Read trimming
- 🧬 Alignment using Bowtie2
- 📊 BAM processing & sorting
- 📈 Gene/transcript quantification (StringTie)
- 📉 Differential expression (edgeR)
- 📊 PCA, Heatmap & Volcano plots
- 🌐 Interactive HTML report
- ♻️ Resume support using checkpoints
- ⚙️ Auto tool installation (conda/apt/R)

---

# ⚡ Pipeline Overview


SRA → FASTQ → QC → Trimming → Alignment → BAM Processing → Counting → DEG → Visualization → Report


---

# 📦 Installation

## 🥇 Recommended (Conda)

```bash
git clone https://github.com/yourname/pranomics.git
cd pranomics

conda env create -f environment.yml
conda activate pranomics

pip install .
🧪 Developer Mode
pip install -e .
🐳 Docker (Optional)
docker build -t pranomics .
docker run -v $PWD:/data pranomics run
▶️ Usage
🧬 Initialize project
pranomics init

Creates required folders:

data/
metadata/
reference/
counts/
DEG/
report/
🚀 Run full pipeline (auto mode)
pranomics run

Automatically:

Detects samples
Validates metadata
Runs full pipeline
Generates report
⚙️ Manual pipeline
pranomics pipeline \
  --samples data \
  --metadata metadata/metadata.csv \
  --reference-dir reference \
  --threads 4
📊 Differential Expression only
pranomics deg \
  --counts counts/gene_count_matrix.csv \
  --metadata metadata/metadata.csv \
  --control Control \
  --treatment Treatment
📊 Outputs

After execution:

🧬 DEG results
DEG/
 ├── DE_results.csv
 ├── upregulated.csv
 ├── downregulated.csv
 ├── summary.txt
📈 Visualizations
PCA plot
Heatmap
Volcano plot (interactive + static)
🌐 Report
report/pranomics_Report.html
🧠 Requirements
System tools (auto-installed if missing)
FastQC
Bowtie2
Samtools
StringTie
SRA-tools
Java
R + edgeR
Python
pandas
numpy
plotly
rich
🧬 Example Metadata
sample,condition
SRR5967160,Control
SRR5967162,Control
SRR5967168,Treatment
📌 Notes
Designed for Linux (Ubuntu/WSL recommended)
Works best with conda environment
Supports resume via checkpoint system
Large datasets recommended on SSD
⚠️ Disclaimer

This tool wraps multiple third-party bioinformatics tools. Ensure proper installation and citation of:

FastQC
Bowtie2
Samtools
StringTie
edgeR (Bioconductor)
📜 License

MIT License © 2026 Gourav Bairagi

See LICENSE file for details.

👨‍💻 Author

Gourav Bairagi
RNA-seq Pipeline Developer