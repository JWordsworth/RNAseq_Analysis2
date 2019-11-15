import os, glob
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict


working_directory = r'/media/njw262/DATA/RNAseq_Analysis'

data_set = 'pantazi_data'

pantazi_folder = os.path.join(working_directory, data_set)

print('pantazi', pantazi_folder)

print (os.path.isdir(pantazi_folder))

if not os.path.isdir(pantazi_folder):
    os.makedirs(pantazi_folder)

url = r'https://www.ebi.ac.uk/ena/data/view/PRJNA526214'


r = requests.get(url)




soup = BeautifulSoup(r.text, features="html.parser")

link_list = []
for link in soup.select("gwt-Anchor"):
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


fname = os.path.join(pantazi_folder, 'download_pantazi_data.sh')

with open(fname, 'w') as f:
    f.write(s)



#ran in command line ../download campisi_data.sh











