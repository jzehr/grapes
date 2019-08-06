#!/bin/bash

## this will cat the appropriate files for GVA
rm data/GVA/GVA_coat_protein_temp_cat.fasta

cat data/GVA/GVA_truncated_coat_protein.fasta\
    data/GVA/GVA_coat_protein.fasta > data/GVA/GVA_coat_protein_temp_cat.fasta