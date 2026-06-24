Pranomics

Automated RNA-seq pipeline:
FASTQ → QC → Alignment → Counts → Differential Expression → Report

🚀 Installation
🥇 Recommended (Docker)
git clone https://github.com/yourname/pranomics.git
cd pranomics
docker build -t pranomics .
docker run -v $PWD:/data pranomics run
🥈 Conda (advanced users)
conda env create -f environment.yml
conda activate pranomics
pip install -e .
pranomics run
🥉 Developer mode
pip install -e .
pranomics run
⚙️ Commands
pranomics init     # create project
pranomics run      # auto pipeline
pranomics pipeline # manual mode
pranomics deg      # DEG only
📊 Output
DEG results
PCA plots
Heatmap
Volcano plot
HTML report
