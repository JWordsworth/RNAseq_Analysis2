import os, glob
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict


working_directory = r'/home/njw262/Documents/RNAseq_Analysis'

data_set = 'mellone_data'

Mellone_folder = os.path.join(working_directory, data_set)

print('campisi', campisi_folder)

print (os.path.isdir(campisi_folder))

if not os.path.isdir(campisi_folder):
    os.makedirs(campisi_folder)

url = r'https://www.ebi.ac.uk/arrayexpress/experiments/E-MTAB-5403/samples/?s_page=1&s_pagesize=500'


r = requests.get(url)




soup = BeautifulSoup(r.text, features="html.parser")

link_list = []
for link in soup.select(".col_26>a"):
    link_list.append(link.get('href'))

# id_list = []
# for link in soup.select('.col_1'):
#     id_list.append(link.text)
#
#
# links_dict = OrderedDict(zip(id_list, link_list))
#
#
# print(links_dict['C1'])




# ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR180/008/ERR1805188/ERR1805188_1.fastq.gz


# print(link_list)

'''

wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR180/008/ERR1805188/ERR1805188_1.fastq.gz

'''

s = ''
s2 = ''
for a in link_list:
    s = s + "wget " + a + '\n'
    s2 += "wget {}\n".format(a)


fname = os.path.join(campisi_folder, 'download_campisi_data.sh')

with open(fname, 'w') as f:
    f.write(s)



#ran in command line ../download campisi_data.sh











