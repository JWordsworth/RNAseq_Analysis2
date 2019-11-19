#!/usr/bin/bash
conda activate py36
echo Tryong to copy
cp "/mnt/storage/nobackup/njw262/RNAseq_Analysis2/aarts_data/data/fastq/SRR6048236_pass_1.fastq" "$TMPDIR/SRR6048236_pass_1.fastq"
echo "sucessfulyl copies"
salmon quant -p 4 -l A -i "/mnt/storage/nobackup/njw262/RNAseq_Analysis2/transcripts_index" -r "$TMPDIR/SRR6048236_pass_1.fastq" -o "$TMPDIR/SRR6048236_pass_1_output" --validateMappings 
