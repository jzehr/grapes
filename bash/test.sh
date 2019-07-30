#!/bin/bash

cat=( GPGV two 3 4 5 )

for i in ${cat[@]}
do
    echo "cat_$i.sh"
done