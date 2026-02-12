# 🔬 AG Schmidt-Ott Omics Hub

An automated multi-omics analysis platform designed for HPC environments. This tool streamlines complex bioinformatics workflows into a user-friendly GUI.

## 🌟 Key Features
* **One-Click Workflows**: Integration with nf-core/rnaseq and CellRanger (GEX/ATAC/CRISPR).
* **Auto-Port Detection**: Intelligent socket binding to prevent port conflicts on shared nodes.
* **HPC Ready**: Native support for SLURM job submission and resource management.
* **Reproducible**: Centralized environment via Miniforge/Conda.

## 🚀 Quick Start
To launch the platform on the cluster, run:
```bash
sbatch RNAseq_app.sh
# or
sbatch Cellranger_app.sh
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
📜 Citation & Acknowledgement
If this tool assists your research, please:

Cite this repository using the "Cite this repository" button on the right.

Acknowledge the development work in your publication's "Acknowledgements" section.

For significant contributions to a project, co-authorship is expected.
