import os




list1 = open("/media/njw262/DATA/RNAseq_Analysis/casella_data/Reference_folder/SRR_List.txt").readlines()
#print(list1)

list2 = ""
for items in list1:
    list2 += "./fastq-dump -I --split-files {} --outdir /media/njw262/DATA/RNAseq_Analysis/casella_data\n".format(items.strip())

working_directory = r'/media/njw262/DATA/RNAseq_Analysis/casella_data/'

fname = os.path.join(working_directory, 'download_casella_data.sh')

with open(fname, 'w') as f:
    f.write(list2)


## If you haven't added the SRA toolkit to your global environment, you will need to run the shell script from the directory of the SRA toolkit