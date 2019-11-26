#!/usr/bin/bash
home="/mnt/nfs/home/njw262"
python download_SRR_parallel.py "/media/njw262/DATA/RNAseq_Analysis2/berger_data/PRJNA231731.txt" --output_directory "/media/njw262/DATA/RNAseq_Analysis2/berger_data/data/sra" --N 4
