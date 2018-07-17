#!/bin/bash

# Full db import
docker run --env=NEO4J_dbms.directories.import=/import --env=NEO4J_dbms_memory_heap_maxSize=5G --volume=$HOME/neo4j/import:/import --volume=$HOME/neo4j/data:/data neo4j:latest /var/lib/neo4j/bin/neo4j-admin import --nodes:Entity=/import/entities.csv --nodes:Sentence=/import/sentences.csv --nodes:Document=/import/documents.csv --nodes:Theme=/import/predicates_0.csv --nodes:Theme=/import/predicates_1.csv --nodes:Theme=/import/predicates_2.csv --nodes:Theme=/import/predicates_3.csv --relationships:IN_SENTENCE=/import/in_sentence.csv --relationships:IN_DOCUMENT=/import/in_document.csv --relationships:HAS_THEME=/import/has_predicate.csv --relationships:STATEMENT=/import/statements_0.csv --relationships:STATEMENT=/import/statements_1.csv --relationships:STATEMENT=/import/statements_2.csv --relationships:STATEMENT=/import/statements_3.csv --database=graph.db

# Test Import
#docker run --env=NEO4J_dbms.directories.import=/import --env=NEO4J_dbms_memory_heap_maxSize=5G --volume=$HOME/neo4j/import:/import --volume=$HOME/neo4j/data:/data neo4j:latest /var/lib/neo4j/bin/neo4j-admin import --nodes:Entity=/import/entities.csv --relationships:STATEMENT=/import/statements_0.csv --relationships:STATEMENT=/import/statements_1.csv --relationships:STATEMENT=/import/statements_2.csv --relationships:STATEMENT=/import/statements_3.csv --database=graph.db

# Be sure to chage paths to match your file tree when running.
