import os, glob
import argparse
import subprocess


def get_fastq_files_unpaired(directory):
    return glob.glob(os.path.join(directory, '*.1.fastq'))


def get_fastq_files_paired(directory):
    ones = glob.glob(os.path.join(directory, '*.1.fastq'))
    twos = glob.glob(os.path.join(directory, '*.2.fastq'))
    return zip(ones, twos)


def build_job_scripts_single(fastq_files, index_dir, output_directory):

    for fastq in fastq_files:
        accession_minus_extension = os.path.splitext(fastq)[0]
        accession = os.path.split(accession_minus_extension)[1]
        job_script =  accession + '.sh'

        shebang = '#!/usr/bin/bash'
        conda = 'conda activate py36'
        copy = f'cp {fastq} $TMPDIR'

        temp_fastq_file = f'$TMPDIR/{accession}.fastq'
        temp_output = f'$TMPDIR/{accession}'
        salmon = f'salmon quant -p 4 -l A -i {index_dir} --output {temp_output} --validateMappings -r {temp_fastq_file}'

        with open(job_script, 'w') as f:
            string = f'{shebang}\n{conda}\n{copy}\n{temp_fastq_file}\n{salmon}'
            f.write(string)
        copy_results_command = f'cp -R {temp_output} {output_directory}'
        os.system(copy_results_command)



def build_job_scripts_double():
    pass


def run():
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Salmonify a set of fastq files')
    parser.add_argument('fastq_dir', help='The directory containing your fastq files')
    parser.add_argument('out_dir', help='The directory to store your results')
    parser.add_argument('--paired', help='When specified, stores True and you will run a paired analysis', action='store_true')
    args = parser.parse_args()


    index_folder = '/mnt/storage/nobackup/njw262/RNAseq_Analysis2/transcripts_index'


    # code for paired
    if args.paired:
        fastq_files = get_fastq_files_paired(args.fastq_dir)

    # code for unpaired
    else:
        fastq_files = get_fastq_files_unpaired(args.fastq_dir)
        build_job_scripts_single(fastq_files, index_folder, args.out_dir)





















