import os, glob
import argparse
import subprocess


def get_fastq_files_single(directory):
    return glob.glob(os.path.join(directory, '*1.fastq'))


def get_fastq_files_double(directory):
    ones = glob.glob(os.path.join(directory, '*1.fastq'))
    twos = glob.glob(os.path.join(directory, '*2.fastq'))
    return zip(ones, twos)



def build_job_scripts_single(fastq_files, index_dir, output_directory):
    for fastq in fastq_files:
        print('running "{}"'.format(fastq))

        if not os.path.isfile(fastq):
            raise FileNotFoundError(fastq)

        accession_minus_extension = os.path.splitext(fastq)[0]
        accession = os.path.split(accession_minus_extension)[1]
        job_script = accession + '.sh'

        shebang = '#!/usr/bin/bash'
        conda = 'conda activate py36'
        temp_fastq_file = f'$TMPDIR/{accession}.fastq'
        copy = f'cp "{fastq}" "{temp_fastq_file}"'

        temp_output = f'"$TMPDIR/{accession}"'
        salmon = f'salmon quant -p 4 -l A -i "{index_dir}" -r "{temp_fastq_file}" -o {temp_output} --validateMappings '
        copy_results_command = f'cp -R "{temp_output}" "{output_directory}"'

        with open(job_script, 'w') as f:
            string = f'{shebang}\n' \
                     f'{conda}\n' \
                     f'{copy}\n' \
                     f'{salmon}\n' \
                     f'{copy_results_command}\n'
            f.write(string)

        os.system('sbatch {}'.format(job_script))
        os.remove(job_script)

def build_job_scripts_double(fastq_files, index_dir, output_directory):
    for fastq1, fastq2 in fastq_files:

        if not os.path.isfile(fastq1):
            raise FileNotFoundError(fastq1)
        if not os.path.isfile(fastq2):
            raise FileNotFoundError(fastq2)

        print(fastq1, fastq2)

        accession_minus_extension = os.path.splitext(fastq1)[0]
        # accession = os.path.split(accession_minus_extension)[1]
        # job_script = accession + '.sh'
        #
        # shebang = '#!/usr/bin/bash'
        # conda = 'conda activate py36'
        # temp_fastq_file = f'$TMPDIR/{accession}.fastq'
        # copy1 = f'cp "{fastq1}" "{temp_fastq_file}"'
        # copy2 = f'cp "{fastq2}" "{temp_fastq_file}"'
        #
        # temp_output = f'"$TMPDIR/{accession}"'
        # salmon = f'salmon quant -p 4 -l A -i "{index_dir}" -r "{temp_fastq_file}" -o {temp_output} --validateMappings '
        # copy_results_command = f'cp -R "{temp_output}" "{output_directory}"'
        #
        # with open(job_script, 'w') as f:
        #     string = f'{shebang}\n' \
        #              f'{conda}\n' \
        #              f'{copy}\n' \
        #              f'{salmon}\n' \
        #              f'{copy_results_command}\n'
        #     f.write(string)
        #
        # os.system('sbatch {}'.format(job_script))
        # os.remove(job_script)





def run():
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Salmonify a set of fastq files')
    parser.add_argument('fastq_dir', help='The directory containing your fastq files')
    parser.add_argument('out_dir', help='The directory containing your result files')
    parser.add_argument('--paired', help='When specified, stores True and you will run a paired analysis',
                        action='store_true')
    args = parser.parse_args()

    index_folder = '/mnt/storage/nobackup/njw262/RNAseq_Analysis2/transcripts_index'

    if args.paired:
        pass

    else:
        print('running unpaired salmon')
        fastq_files = get_fastq_files_single(args.fastq_dir)
        build_job_scripts_single(fastq_files, index_folder, args.out_dir)
