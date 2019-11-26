import os, glob
import argparse
import subprocess


def get_sra_files(directory):
    return glob.glob(os.path.join(directory, '*.sra'))


def create_run_scripts(sra_files, output_directory):
    """
    create run scripts for slurm job scheduler

    :param sra_files:
    :param output_directory:
    :return:
    """
    if not isinstance(sra_files, list):
        raise ValueError('sra_files: {}\ntype: {}'.format(sra_files, type(sra_files)))

    shebang = '#!/usr/bin/bash'
    conda_cmd = 'conda activate py36'
    job_scripts = []
    for sra_file in sra_files:
        # print('submitting "{}"'.format(sra_file))
        # print(sra_file)
        job_script = os.path.splitext(sra_file)[0]
        # print(job_script)
        job_script = os.path.split(job_script)[1]
        job_script += '.sh'

        cmd = f'fastq-dump {sra_file} --outdir {output_directory} --split-files --readids -origfmt --clip --read-filter pass'
        # print(cmd)

        with open(job_script, 'w') as f:
            full_command = f'{shebang}\n{conda_cmd}\n{cmd}'
            print(full_command)
            print('\n')
            f.write(full_command)

        job_scripts.append(job_script)
    return job_scripts


def run_with_slurm(job_scripts):
    for script in job_scripts:
        os.system('sbatch {}'.format(script))
        os.remove(script)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert directory of SRA files into fastq')
    parser.add_argument('sra_dir', help='The directory containing your SRA files')
    parser.add_argument('fastq_dir', help='The directory to put your fastq files')
    args = parser.parse_args()


    sra_files = get_sra_files(args.sra_dir)


    job_scripts = create_run_scripts(sra_files, args.fastq_dir)

    run_with_slurm(job_scripts)
