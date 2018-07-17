#!/bin/bash

# mkdir -p ../data

BASE_DATA="../data"
SCRIPT_DIR="./neo4j"

# mkdir -p ${BASE_DATA}"/neo4j"
NEO_DIR=${BASE_DATA}"/neo4j"
GNBR_DIR=${BASE_DATA}"/GNBR/"

# Make neo4j directories.
mkdir -p ${NEO_DIR}/import/ 
# ${NEO_DIR}/data/ ${NEO_DIR}/logs/

# Generate concepts files.
python3 ${SCRIPT_DIR}/entities.py $GNBR_DIR ${NEO_DIR}/import/entities.csv
python3 ${SCRIPT_DIR}/sentences.py $GNBR_DIR ${NEO_DIR}/import/sentences.csv
python3 ${SCRIPT_DIR}/predicates.py $GNBR_DIR ${NEO_DIR}/import/predicates.csv

# Generate relationships files
python3 ${SCRIPT_DIR}/statements.py $GNBR_DIR ${NEO_DIR}/import/statements.csv 
python3 ${SCRIPT_DIR}/entity_in_sentence.py $GNBR_DIR ${NEO_DIR}/import/in_sentence.csv
python3 ${SCRIPT_DIR}/sentence_has_predicate.py $GNBR_DIR ${NEO_DIR}/import/has_predicate.csv

# python3 documents.py ../../data/GNBR/ ../../data/Pubmed/PMID_2_year_Master.txt ../../data/neo4j/import/documents.csv ../../data/neo4j/import/in_document.csv
