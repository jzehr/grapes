#!/bin/bash

## this will cat the appropriate files for GPGV
rm data/GPGV/GPGV_coat_protein_cat.fasta

cat data/GPGV/GPGV_CP.fasta\
    data/GPGV/GPGV_coat_protein.fasta > data/GPGV/GPGV_coat_protein_cat.fasta
