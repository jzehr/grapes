#!/bin/bash

## this will cat the appropriate files for GPGV
rm data/GPGV/GPGV_coat_protein_temp_cat.fasta

cat data/GPGV_CP.fasta\
    data/GPGV_coat_protein.fasta > data/GPGV_coat_protein_temp_cat.fasta
