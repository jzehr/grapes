#!/bin/bash

## cat the proper files together
cat ../../data/GLRaV3/GLRaV3_35_kDa_coat_protein.fasta ../../data/GLRaV3/GLRaV3_major_coat_protein.fasta ../../data/GLRaV3/GLRaV3_coat_protein.fasta > ../../data/GLRaV3/GLRaV3_coat_protein_cat.fasta

## run it through the hyphy batch file 
hyphy ../../hyphy-analyses/codon-msa/pre-msa.bf --input ../../data/GLRaV3/GLRaV3_coat_protein_cat.fasta

## remove old files
rm -rf ../../data/GLRaV3/GLRaV3_coat_protein_protein_align.fasta.ckp.gz

## align the file with mafft
mafft --amino ../../data/GLRaV3/GLRaV3_coat_protein_cat.fasta_protein.fas > ../../data/GLRaV3/GLRaV3_coat_protein_protein_align.fasta

## build the tree with iqtree
iqtree -s ../../data/GLRaV3/GLRaV3_coat_protein_protein_align.fasta
