#!/bin/bash

## this will cat the appropriate files for GLRaV3
echo "removing any pre-existing files"

FILE=data/GLRaV3_coat_protein_temp_cat.fasta
if test -f "$FILE"; then
    echo "blah"
    rm "$FILE"
else
    echo "other"
    cat data/GLRaV3_35_kDa_coat_protein.fasta\
        data/GLRaV3_major_coat_protein.fasta\
        data/GLRaV3_CP.fasta\
        data/GLRaV3_coat_protein.fasta > data/GLRaV3_coat_protein_temp_cat.fasta
fi



## for coat protein ## 