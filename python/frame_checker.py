import subprocess
import json
import argparse
from Bio  import SeqIO
import signal

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="path to your CAT_REGION_PRODS.json", type=str)
args = parser.parse_args()

in_file = args.file

'''

write a function that will:
1. read in the catted file
2. test to see if it errors out immediately
3. remove the file after the test

'''



HYPHY = "~/grapes/hyphy-develop/hyphy LIBPATH=/home/jordanz/grapes/hyphy-develop/res"
PRE = "~/grapes/hyphy-analyses/codon-msa/pre-msa.bf"


## check to see if NO seqs are divisible by 3
# then return error
def frame_checker(key, value):
    inf = "data/fasta/cat_%s_%s.fasta" % (key, value)
    '''
    try:
        subprocess.call("%s %s --input %s" % (HYPHY, PRE, inf), terminal=True)
        signal.alarm(5)
    except:
        print(f"this key {key} is messed up")

    #subprocess.call("rm %s" % inf)

    seqs = []
    for record in SeqIO.parse(inf, "fasta"):
        seqs.append(record.seq)

    yes = []
    no = []
    for s in seqs:
        if len(s) % 3 == 0:
           yes.append(1)
        else:
            no.append(1)

    print(f" {key} this is yes {sum(yes)} this is no {sum(no)}\n")
    if not sum(yes) > 0:
        print(f"{key} no in frame")
    '''

with open(in_file) as j_file:
    data = json.load(j_file)

for key, value in data.items():
    frame_checker(key, value)



