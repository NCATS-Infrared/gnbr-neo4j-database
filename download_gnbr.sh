#!/bin/bash

FILES=(\
part-i-chemical-disease-path-theme-distributions.txt.gz \
part-i-chemical-gene-path-theme-distributions.txt.gz \
part-i-gene-gene-path-theme-distributions.txt.gz \
part-ii-dependency-paths-chemical-disease-sorted-with-themes.txt.gz \
part-ii-dependency-paths-chemical-gene-sorted-with-themes.txt.gz \
part-ii-dependency-paths-gene-disease-sorted-with-themes.txt.gz \
part-ii-dependency-paths-gene-gene-sorted-with-themes.txt.gz\
)

# Set GNBR download url and folder
BASE_URL="https://zenodo.org/record/1243969/files"
DWNLD_DIR="$HOME/gnbr"
NEO_DATA_DIR="$HOME/neo4j"


mkdir -p $DWNLD_DIR $NEO_DATA_DIR
for file in "${FILES[@]}";
do echo $file;
done | xargs -P 2 -n 1 -I foo curl ${BASE_URL}/foo -o ${DWNLD_DIR}/foo


python -m format_gnbr ${DWNLD_DIR} ${NEO_DATA_DIR}

