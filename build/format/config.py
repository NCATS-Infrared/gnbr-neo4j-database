
DWNLD_DIR="~/test/gnbr"
NEO_DATA_DIR="~/test/neo4j"

FULL_BUILD=True # Flag for full or minimal instance (entities and statements only)


"""
Download URLS and destinations
"""

URLS=[
"https://zenodo.org/record/1243969/files/part-i-chemical-disease-path-theme-distributions.txt.gz",
"https://zenodo.org/record/1243969/files/part-i-chemical-gene-path-theme-distributions.txt.gz",
"https://zenodo.org/record/1243969/files/part-i-gene-disease-path-theme-distributions.txt.gz",
"https://zenodo.org/record/1243969/files/part-i-gene-gene-path-theme-distributions.txt.gz",
"https://zenodo.org/record/1243969/files/part-ii-dependency-paths-chemical-disease-sorted-with-themes.txt.gz",
"https://zenodo.org/record/1243969/files/part-ii-dependency-paths-chemical-gene-sorted-with-themes.txt.gz",
"https://zenodo.org/record/1243969/files/part-ii-dependency-paths-gene-disease-sorted-with-themes.txt.gz",
"https://zenodo.org/record/1243969/files/part-ii-dependency-paths-gene-gene-sorted-with-themes.txt.gz"
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


"""
Output headers
"""
ENTITY_HEADER = ['uri:ID(Entity-ID)', 'name', 'type']

SUBJECT_ID = ['subj_id']
SUBJECT_LABEL = ['subj_type']
SUBJECT_INFO = ['subj_id', 'subj_name', 'subj_type']

OBJECT_ID = ['obj_id']
OBJECT_LABEL = ['obj_type']
OBJECT_INFO = ['obj_id', 'obj_name', 'obj_type']


SENTENCE_HEADER = [':ID(Sentence-ID)', 'pmid', 'loc', 'text']
SENTENCE_ID = ['text']
SENTENCE_INFO = ['pmid', 'loc', 'text']

DOCUMENT_HEADER = []
DOCUMENT_ID_FIELD = ['pmid']


THEME_HEADER = [':ID(Path-ID)', ':LABEL']
THEME_ID = ['path']
THEME_LABEL = ['subj_type', 'obj_type']


IN_SENTENCE_HEADER = [':START_ID(Entity-ID)', 'raw_string', ':END_ID(Sentence-ID)']
SUBJECT_MENTION = ['subj_id', "subj_name_raw"]
OBJECT_MENTION = ['obj_id', "obj_name_raw"]

IN_DOCUMENT_HEADER = []

HAS_THEME_HEADER = [':START_ID(Sentence-ID)',':END_ID(Path-ID)', 'path']
HAS_THEME_INFO = ['path']

STATEMENT_HEADER = [":START_ID(Entity-ID)", ":END_ID(Entity-ID)"]

"""
ID Fields
"""



CMD_LINE_ERROR="""\
Error: wrong number of arguments, check usage statement below:\n\n
USAGE: python script.py <path/to/dwnld/> <path/to/import>
"""