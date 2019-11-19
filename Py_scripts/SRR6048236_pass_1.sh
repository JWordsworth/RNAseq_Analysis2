#!/usr/bin/bash
conda activate py36
cp "/mnt/storage/nobackup/njw262/RNAseq_Analysis2/aarts_data/data/fastq/SRR6048236_pass_1.fastq" "$TMPDIR/SRR6048236_pass_1.fastq"
salmon quant -p 4 -l A -i /mnt/storage/nobackup/njw262/RNAseq_Analysis2/transcripts_index -r "$TMPDIR/SRR6048236_pass_1.fastq" --output "$TMPDIR/SRR6048236_pass_1" --validateMappings 