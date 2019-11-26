import os, glob
import numpy as np
import argparse
import multiprocessing as mp
import time
import subprocess
import pandas


def get_accession_list(filename):

    Import_data = pandas.read_csv(filename, sep="\t")
    if not 'sra_ftp' in Import_data.columns:
        raise ValueError("You don't have the column title: sra_ftp")
    ftp1 = Import_data.loc[:, "sra_ftp"]
    # print(ftp1)
    # print("bum")
    ftp2 = list(ftp1)
    # print(ftp2)
    new_list = []
    for address in ftp2:
        if ";" in address:
            new_list += address.split(";")
            # print(address)
        else:
            new_list.append(address)
    print(len(new_list))
    return(new_list)


#dikovskaya = get_accession_list("/media/njw262/DATA/RNAseq_Analysis2/dikovskaya_data/PRJNA289328.txt")
# print(dikovskaya)

def process_accession_file(filename):
    """
    Turn text fie containing list of SRA accession numbers into usable python list.

    This is obsolete, we changed it because it didnt work
    Deperecated
    :param filename:
    :return:
    """
    with open(filename, 'r') as f:
        text = f.read()

    # cater for the case when there is only 1 accession in the file
    if '\n' not in text:
        return [text]

    accession_list = text.split('\n')

    accession_list = [i for i in accession_list if i != '']

    return accession_list

    #Also obsolete:
def build_urls(accession_list):
    base_url = r'ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR'
    first_three = [i[:6] for i in accession_list]
    urls = []
    for i in range(len(accession_list)):
        first = first_three[i]
        second = accession_list[i]
        urls.append(f'{base_url}/{first}/{second}/{second}.sra')

    return urls


def create_lists_for_parallel_download(urls, N):
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


def download_using_wget(accession_list, directory):
    """
    Build list of wget commands to download accession list sequentially
    :param accession_list:
    :return:
    """
    s = np.random.uniform(1, 10)
    time.sleep(s)
    if not os.path.isdir(directory):
        os.makedirs(directory)


    command_list = []
    for ftp_url in accession_list:
        _, accession = os.path.split(ftp_url)
        if not os.path.isfile(ftp_url):

            # --random-wait
            # --wait=seconds
            command_list.append(f'wget {ftp_url} -O {directory}/{accession}.sra')
        else:
            print(f'{ftp_url} already exists. Bypassing.')

    for ftp_url in command_list:
        try:
            if not os.path.isfile(ftp_url):
                subprocess.check_call([ftp_url], shell=True)
        except:
            print('broken command: ' + ftp_url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('sra_accession_file', type=str, help='text file containing list of SRR accessions to download')
    parser.add_argument('--N', default=1, type=int, help='number of processes to use for downloading')
    parser.add_argument('--output_directory', type=str, default='.')
    args = parser.parse_args()

    fle = r'/media/njw262/DATA/RNAseq_Analysis/Py_scripts/srr_file'



    # The N variable determines how many separate processes to use for downloading in parallel
    # N = 4
    #
    # # read accessions into python
    # accessions = process_accession_file(args.sra_accession_file)
    #
    # # build urls using accession files
    # urls = build_urls(accessions)
    #
    # # split the list into N sub lists which will be processed independently

    urls = get_accession_list(filename=args.sra_accession_file)


    sublist_of_urls = create_lists_for_parallel_download(urls, args.N)

    # print(sublist_of_urls)

    processes = [mp.Process(target=download_using_wget, args=(sublist, args.output_directory)) for sublist in sublist_of_urls]

    for p in processes:
        p.start()

    for p in processes:
        p.join()




