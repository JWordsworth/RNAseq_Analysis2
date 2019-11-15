#for root, directories, filenames in os.walk("~/Documents/RNAseq_Analysis/campisi_data"):
 #   slist = []
  #  for filename in filenames:
   #     slist += filename

import subprocess
import glob
import os
import gzip
import shutil

dir_name = r"/media/njw262/DATA/RNAseq_Analysis/casella_data/Fastq_files"



# extension = ".zip"

# files = glob.glob(os.path.join(dir_name, '*.gz'))
# slist = ''
# for file in files:
#     slist += "gunzip " + file + "\n"
# #print(slist)
#
# fname = os.path.join(dir_name, 'unzip_folders2.sh')
#
# with open(fname, 'w') as f:
#     f.write(slist)


# os.chdir(dir_name)

#for filename in files:
    # if filename.endswith('.gz'):
        # print(filename)
    #file_name = os.path.abspath(filename)
    # print(file_name)
    #zip_ref = zipfile.ZipFile(file_name)
    #zip_ref.extractall(dir_name)
    #zip_ref.close()
    # os.remove(file_name)




'''

salmon quant -i ~/Documents/RNAseq_Analysis/transcriptome/transcript_index/ -l A -1 ~/Documents/RNAseq_Analysis/fastq/C1_ATCACG_L001_R1_001.fastq -2 ~/Documents/RNAseq_Analysis/fastq/C1_ATCACG_L001_R2_001.fastq --validateMappings -o transcript_quant_Day0
'''

def salmonify(salmon_file, index, forward, backward):
    forward_directory, forward_file = os.path.split(forward)
    forward_name = forward_file[:-6]
    return "{} quant -i {} " \
            "-l A -1 {} -2" \
            " {} --validateMappings --gcBias --seqBias -o {}".format(
        salmon_file, index, forward, backward, forward_name
    )
salmon_file = '/media/njw262/DATA/Software/salmon-0.12.0_linux_x86_64/bin/salmon'

index_file = '/media/njw262/DATA/RNAseq_Analysis/transcriptome/transcript_index'
#forwards_file = '/media/njw262/DATA/RNAseq_Analysis/campisi_data/Fibroblasts/IR4/ERR1805192_1.fastq'
#bakward_file = '/media/njw262/DATA/RNAseq_Analysis/campisi_data/Fibroblasts/IR4/ERR1805192_2.fastq'

# results = salmonify(salmon_file, index_file, forwards_file, bakward_file)

# print(results)


# os.system(results)

files = glob.glob("/media/njw262/DATA/RNAseq_Analysis/casella_data/Fastq_files/*.fastq")
# print(files)
list1 = []
list2 = []
for fil in sorted(files):
    number = fil[-7]

    # print(number)
    if number == "1":
        list1.append(fil)
    if number == "2":
        list2.append(fil)


for forwards, backwards in zip(list1, list2):
    results = salmonify(salmon_file, index_file, forwards, backwards)
    os.system(results)

    # subprocess.Popen([results])

    # print('i is {}'.format(i))
    # print('j is {}'.format(j))

























