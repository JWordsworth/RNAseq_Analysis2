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
        raise ValueError

    job_scripts = []
    for sra_file in sra_files:
        job_script = os.path.splitext(sra_file)
        job_script = os.path.split(job_script)

        shebang = '#!/usr/bin/bash'
        cmd = f'fastq-dump {sra_file} --outdir {output_directory} --split-files --readids -origfmt --clip --read-filter pass'

        with open(job_script, 'w') as f:
            f.write(f'{shebang}\n{cmd}')

        job_scripts.append(job_script)
    return job_scripts


def run_with_slurm(job_scripts):
    for script in job_scripts:
        cmd = ['sbatch', script]
        subprocess.check_call(cmd, shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert directory of SRA files into fastq')
    parser.add_argument('sra_dir', help='The directory containing your SRA files')
    parser.add_argument('fastq_dir', help='The directory to put your fastq files')
    args = parser.parse_args()

    job_scripts = create_run_scripts(args.sra_dir, args.fastq_dir)

    run_with_slurm(job_scripts)
