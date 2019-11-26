#!/usr/bin/bash
#SBATCH --cpus-per-task=4
home="/mnt/nfs/home/njw262"
source "$home/.bashrc"
conda activate py36
python download_SRR_parallel.py "/mnt/storage/nobackup/njw262/RNAseq_Analysis2/buj_data/PRJNA552100.txt" --output_directory "/mnt/storage/nobackup/njw262/RNAseq_Analysis2/buj_data/data/sra" --N 4
