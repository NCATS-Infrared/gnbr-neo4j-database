"""
Headers for raw GNBR files.
"""

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
ENTITY_HEADER = ['uri:ID(Entity-ID)', 'name', ':LABEL']
SENTENCE_HEADER = [':ID(Sentence-ID)', 'pmid', 'loc', 'text']
DOCUMENT_HEADER = []
THEME_HEADER = []

IN_SENTENCE_HEADER = []
IN_DOCUMENT_HEADER = []
HAS_THEME_HEADER = []
STATEMENT_HEADER = []

"""
ID Fields
"""
SUB_ID_FIELD = ['subj_id']
OBJ_ID_FIELD = ['obj_id']
SENTENCE_ID_FIELD = ['text']
THEME_ID_FIELD = ['path']
DOCUMENT_ID_FIELD = ['pmid']


CMD_LINE_ERROR="""\
Error: wrong number of arguments, check usage statement below:\n\n
USAGE: python script.py <path/to/dwnld/> <path/to/import>
"""