#!/bin/bash

## this will cat the appropriate files for GLRaV3
rm data/GLRaV3/GLRaV3_coat_protein_cat.fasta

cat data/GLRaV3/GLRaV3_35_kDa_coat_protein.fasta\
    data/GLRaV3/GLRaV3_major_coat_protein.fasta\
    data/GLRaV3/GLRaV3_divergent_coat_protein.fasta\
    data/GLRaV3/GLRaV3_coat_protein.fasta > data/GLRaV3/GLRaV3_coat_protein_cat.fasta