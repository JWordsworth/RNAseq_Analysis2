
import glob
import os


dir_name = r"/media/njw262/DATA/RNAseq_Analysis/jung_data/Fastq_files"




def salmonify(salmon_file, index, forward):
    forward_directory, forward_file = os.path.split(forward)
    forward_name = forward_file[:-8]
    return "{} quant -i {} " \
            "-l A -r {}" \
            " --validateMappings --gcBias --seqBias -o {}".format(
        salmon_file, index, forward, forward_name
    )
salmon_file = '/media/njw262/DATA/Software/salmon-0.12.0_linux_x86_64/bin/salmon'

index_file = '/media/njw262/DATA/RNAseq_Analysis/transcriptome/transcript_index'
#forwards_file = '/media/njw262/DATA/RNAseq_Analysis/campisi_data/Fibroblasts/IR4/ERR1805192_1.fastq'
#bakward_file = '/media/njw262/DATA/RNAseq_Analysis/campisi_data/Fibroblasts/IR4/ERR1805192_2.fastq'

# results = salmonify(salmon_file, index_file, forwards_file, bakward_file)

# print(results)


# os.system(results)

files = glob.glob("/media/njw262/DATA/RNAseq_Analysis/jung_data/Fastq_files/*.fastq")
# print(files)
list1 = []
for fil in sorted(files):
    list1.append(fil)
# print(list1, list2)

for fils in list1:
    results = salmonify(salmon_file, index_file, fils)
    os.system(results)

    # subprocess.Popen([results])

    # print('i is {}'.format(i))
    # print('j is {}'.format(j))

























