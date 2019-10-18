import re
from Bio import SeqIO
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
from Bio import Align


#from Bio.Blast import NCBIWWW

import json

from helper import name_fixer
'''
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context
'''


def cds_cleaner(cds):
    orf1_s, orf1_e = int(re.findall(r'\d+', cds.split("..")[0])[0]) - 1, int(re.findall(r'\d+', cds.split("..")[1])[0])
    return orf1_s, orf1_e

'''
read in each region fasta and:
    1. blast each seq to the complete genome ORF
    2. bin the ORF
    3. write to a fasta file
'''

with open("rsrc/GLRaV3_regions.json") as regions_json:
    d = json.load(regions_json)

REGIONS = list(d.keys())
#print(REGIONS)

with open("data/COMPLETE_GENOMES.json") as genomes_json:
    g = json.load(genomes_json)

## just grabbing the first reference genome ##
first = {list(g.keys())[1] : list(g.values())[1]}
key = list(first.keys())[0]
CDS = first[key]["CDS"]
notes = first[key]["note"]
product = first[key]["product"]
nuc_seq = first[key]["nuc_seq"]

## making the ORF dict to blast against ##
ORF_nums = ["1a","1b","2","3","4","5","6","7","8","9","10","11", "12"]
cleaned_CDS = [cds_cleaner(cds) for cds in CDS]
#print(cleaned_CDS)

ORFS = ["ORF" + item + "_" + name_fixer(product[pos]) for pos, item in enumerate(ORF_nums)]


ref_orfs = {}
for pos, item in enumerate(ORFS):
    temp = {}
    s, e = cleaned_CDS[pos][0], cleaned_CDS[pos][1]
    temp[item] = nuc_seq[s:e]
    ref_orfs.update(temp)

refs = list(ref_orfs.values())
print(len(refs))

## time to compare each sequence to

for r in REGIONS[0:1]:
    infas = "data/fasta/%s_all.fasta" % r
    data = []
    for record in SeqIO.parse(infas, "fasta"):
        data.append(record)


    aligner = Align.PairwiseAligner()
    for i in data[0:1]:
        scores = []
        for j in refs:
            scores.append(aligner.score(i.seq, j))
        print(scores)


