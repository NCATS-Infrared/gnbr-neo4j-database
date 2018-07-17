from os.path import expanduser


"""
File locations for raw GNBR files and parsed GNBR files.
"""
import_directory = expanduser('~/gnbr')
output_directory = expanduser('~/neo4j')

"""
Headers for raw GNBR files.
"""

# Header for GNBR part 2 files (entities, sentences, dependency paths).
part_ii_header = [
    "pmid", "loc", 
    "subj_name", "subj_loc", 
    "obj_name", "obj_loc",
    "subj_name_raw", "obj_name_raw", 
    "subj_id", "obj_id", 
    "subj_type", "obj_type", 
    "path", "text"
    ] 


"""
Output headers for cleaned and parsed neo4j import files.
"""

out_header = ['uri:ID(Entity-ID)', 'name', ':LABEL']