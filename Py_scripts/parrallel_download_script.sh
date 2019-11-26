#!/usr/bin/bash
#SBATCH --cpus-per-task=$1
home="/mnt/nfs/home/njw262"
source "$home/.bashrc"
conda activate py36
python download_SRR_parallel.py "/mnt/storage/nobackup/njw262/RNAseq_Analysis2/dikovskaya_data/PRJNA289328.txt" --output_directory "/mnt/storage/nobackup/njw262/RNAseq_Analysis2/dikovskaya_data/data/sra" --N $1
