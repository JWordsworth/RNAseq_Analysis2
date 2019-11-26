import pandas

import os, glob
import argparse
import subprocess
import numpy as np
import multiprocessing as mp


# Process 1
def get_sra_files(directory):
    return glob.glob(os.path.join(directory, '*.sra'))


def create_lists_for_parallel_dumping(urls, N):
    """
    Takes a list of accession numbers and splits them equally into N lists, accounting
    for remainders
    :param urls:
    :param N:
    :return:
    """

    list_size = len(urls)

    # number to download per process
    n_per_process = int(np.floor(list_size / N))

    # account for remainder
    remainder = list_size % N
    number_to_download_per_process = [n_per_process] * N

    for i in range(remainder):
        number_to_download_per_process[i] += 1

    process_list = []
    for i in range(N):
        l = []
        for j in range(number_to_download_per_process[i]):
            l.append(urls.pop())
        process_list.append(l)

    return process_list


def create_fastq_dump(accession_list, directory, sra_tools_bin_directory='/home/njw262/sratoolkit.2.9.4-centos_linux64/bin/'):
    """
    create run scripts for slurm job scheduler

    :param sra_files:
    :param output_directory:
    :return:
    """
    if not isinstance(accession_list, list):
        raise ValueError('sra_files: {}\ntype: {}'.format(accession_list, type(accession_list)))

    environment_variables = os.environ.copy()
    environment_variables['PATH'] = environment_variables['PATH'] + ':' + sra_tools_bin_directory

    for sra_file in accession_list:
        cmd = f'fastq-dump {sra_file} --outdir {directory} --split-files --readids --origfmt --clip --read-filter pass'
        subprocess.check_call(cmd.split(' '), shell=False, env=environment_variables)
        # os.system(cmd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a directory of SRA files into fastq files in parallel')
    parser.add_argument('sra_directory', type=str, help='directory containing SRA files. ')
    parser.add_argument('--N', default=1, type=int, help='number of processes to use for converting')
    parser.add_argument('--output_directory', type=str, default='Where to store the resulting fastq files')
    args = parser.parse_args()

    sra_list = get_sra_files(args.sra_directory)
    sra_list = create_lists_for_parallel_dumping(sra_list, args.N)

    processes = [mp.Process(target=create_fastq_dump, args=(sublist, args.output_directory)) for sublist in sra_list]

    for p in processes:
        p.start()

    for p in processes:
        p.join()
