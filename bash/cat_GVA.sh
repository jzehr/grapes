#!/bin/bash

## this will cat the appropriate files for GVA
#rm data/GVA_coat_protein_temp_cat.fasta
FILE=data/GVA_coat_protein_temp_cat.fasta
if test -f "$FILE"; then
  #echo "blah"
  rm "$File"
fi
cat data/GVA_truncated_coat_protein.fasta \
    data/GVA_coat_protein.fasta > data/GVA_coat_protein_temp_cat.fasta
