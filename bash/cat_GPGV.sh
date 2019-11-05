#!/bin/bash

## this will cat the appropriate files for GPGV
echo "removing any pre-existing files"

FILE=data/GPGV/GPGV_coat_protein_temp_cat.fasta
if test -f "$FILE"; then
   #echo "blah"
    rm "$FILE"
fi
cat data/GPGV_CP.fasta \
    data/GPGV_coat_protein.fasta > data/GPGV_coat_protein_temp_cat.fasta
