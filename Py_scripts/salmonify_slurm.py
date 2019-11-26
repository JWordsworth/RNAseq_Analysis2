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

        out_directory = os.path.join(output_directory, accession)

        shebang = '#!/usr/bin/bash'
        conda = 'conda activate py36'
        temp_fastq_file = f'$TMPDIR/{accession}.fastq'
        copy = f'cp "{fastq}" "{temp_fastq_file}"'

        temp_output = f'$TMPDIR/{accession}'
        salmon = f'salmon quant -p 8 -l A -i "{index_dir}" -r "{temp_fastq_file}" -o {temp_output} --validateMappings '
        copy_results_command = f'cp -R "{temp_output}" "{out_directory}"'

        with open(job_script, 'w') as f:
            string = f'''{shebang}
home="/mnt/nfs/home/njw262"
ref="{index_dir}"
source "$home/.bashrc"
{conda}
{copy}
echo "copied stuff. Rummimg salmon "
tmp_ref="$TMPDIR/ref"
cp -R "$ref" "$tmp_ref"
{salmon}
echo "samon ran it somin else!"
{copy_results_command}
'''
            f.write(string)

        os.system('sbatch --mem-per-cpu=8G {}'.format(job_script))
        # os.remove(job_script)


def extract_accession(fastq_file):
    dire, fle = os.path.split(fastq_file)
    acc, ext = os.path.splitext(fle)
    if acc[-2:] not in ['_1', '_2']:
        raise ValueError('Unexpected extension: "{}"'.format(acc))

    return acc[:-2]

def build_job_scripts_double(fastq_files, index_dir, output_directory):
    for fastq1, fastq2 in fastq_files:

        if not os.path.isfile(fastq1):
            raise FileNotFoundError(fastq1)
        if not os.path.isfile(fastq2):
            raise FileNotFoundError(fastq2)

        if extract_accession(fastq1) != extract_accession(fastq2):
            raise ValueError('Fastq1 does not equal fastq2: "{}" != "{}"'.format(fastq1, fastq2))

        run_accession = extract_accession(fastq1)

        job_script = run_accession + '.sh'

        shebang = '#!/usr/bin/bash'


        # conda = 'conda activate py36'
        temp_fastq1 = f'$TMPDIR/{run_accession}1.fastq'
        temp_fastq2 = f'$TMPDIR/{run_accession}2.fastq'
        temp_index = f'$TMPDIR/index'
        temp_output = f'$TMPDIR/{run_accession}'

        with open(job_script, 'w') as f:
            string = f"""{shebang}
bash_rc=/mnt/nfs/home/njw262/.bashrc
source $bash_rc
conda activate py36
cp "{fastq1}" "{temp_fastq1}" 
cp "{fastq2}" "{temp_fastq2}"
cp -R "{index_dir}" "{temp_index}"
salmon quant -p 8 -l A -i "{temp_index}" -1 "{temp_fastq1}" -2 "{temp_fastq2}" -o "{temp_output}" --validateMappings
cp -R "{temp_output}" "{output_directory}"
"""
            f.write(string)

        os.system('sbatch --mem-per-cpu=8G {}'.format(job_script))
        # os.remove(job_script)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Salmonify a set of fastq files')
    parser.add_argument('fastq_dir', help='The directory containing your fastq files')
    parser.add_argument('out_dir', help='The directory containing your result files')
    parser.add_argument('--paired', help='When specified, stores True and you will run a paired analysis',
                        action='store_true')
    args = parser.parse_args()

    index_folder = '/mnt/storage/nobackup/njw262/RNAseq_Analysis2/transcripts_index'

    # create the output parent directory fi not exist
    if not os.path.isdir(args.out_dir):
        os.makedirs(args.out_dir)

    if args.paired:
        print("Running paired analysis")
        fastq_files = get_fastq_files_double(args.fastq_dir)
        build_job_scripts_double(fastq_files, index_folder, args.out_dir)


    else:
        print('running unpaired salmon')
        fastq_files = get_fastq_files_single(args.fastq_dir)
        build_job_scripts_single(fastq_files, index_folder, args.out_dir)
