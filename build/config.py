
# Directory in which to download raw GNBR files
DWNLD_DIR="~/neo4j/gnbr"

# Directory in which to output GNBR files formatted for neo4j import
NEO_DATA_DIR="~/neo4j/import"


# Raw GNBR file URLs
URLS=[
"https://zenodo.org/record/1495808/files/part-i-chemical-disease-path-theme-distributions.txt.zip",
"https://zenodo.org/record/1495808/files/part-i-chemical-gene-path-theme-distributions.txt.zip",
"https://zenodo.org/record/1495808/files/part-i-gene-disease-path-theme-distributions.txt.zip",
"https://zenodo.org/record/1495808/files/part-i-gene-gene-path-theme-distributions.txt.zip",
"https://zenodo.org/record/1495808/files/part-ii-dependency-paths-chemical-disease-sorted-with-themes.txt.zip",
"https://zenodo.org/record/1495808/files/part-ii-dependency-paths-chemical-gene-sorted-with-themes.txt.zip",
"https://zenodo.org/record/1495808/files/part-ii-dependency-paths-gene-disease-sorted-with-themes.txt.zip",
"https://zenodo.org/record/1495808/files/part-ii-dependency-paths-gene-gene-sorted-with-themes.txt.zip"
]

# Header for GNBR part 2 files (entities, sentences, dependency paths).
HEADER = [
    "pmid", "loc", 
    "subj_name", "subj_loc", 
    "obj_name", "obj_loc",
    "subj_name_raw", "obj_name_raw", 
    "subj_id", "obj_id", 
    "subj_type", "obj_type", 
    "path", "text"
    ] 


# Names for output files
FILES = {
	'entities': 'entity.csv.gz',
	'mentions': 'mention.csv.gz',
	'sentences': 'sentence.csv.gz',
	'themes': 'theme.csv.gz',
	'has_mentions': 'has_mention.csv.gz',
	'in_sentences': 'in_sentence.csv.gz',
	'has_themes': 'has_theme.csv.gz',
	'statements': 'statement.csv.gz'
}


CMD_LINE_ERROR="""\
Error: wrong number of arguments, check usage statement below:\n\n
USAGE: python script.py <path/to/dwnld/> <path/to/import>
"""