import time
import gzip
import hashlib
import sys
import csv
import os

# Check input and print usage if number of arguments is invalid
if len(sys.argv) != 5:
	print("Error: wrong number of arguments, check usage statement below:\n")
	print("USAGE: python GNBR_2_csv.py <path/to/part-ii-files/> <path/to/citations.txt/> <path/to/documents.csv> <path/to/relations.csv>")
	exit()

# Define input and output headers

in_header = [
    "pmid", "loc", 
    "subj_name", "subj_loc", 
    "obj_name", "obj_loc",
    "subj_name_raw", "obj_name_raw", 
    "subj_id", "obj_id", 
    "subj_type", "obj_type", 
    "path", "text"
    ] 

out_header = ['pmid:ID(Document-ID)', 'year:int']
id_fields = ['text']

rela_header = [':START_ID(Sentence-ID)', ':END_ID(Document-ID)']


# Handy subroutines
def filepath( filename ):
    return import_dir+'/'+filename 

def hash_md5(array):
    return hashlib.md5( ''.join(array).encode() ).hexdigest()

def open_csv(name, delimiter=','):
    return csv.writer(open('{}'.format(name), 'wt'), doublequote=True, delimiter=delimiter, escapechar='\\')

def get_fields(line, fields, header):
    extractor = dict( zip(header, line) )
    return [extractor[i] for i in fields]

# Get file info from arguments
import_dir = sys.argv[1]
citations_file = sys.argv[2]
part_ii_files = [f for f in os.listdir(import_dir) if '-ii-' in f]
outFile = sys.argv[3]
relaFile = sys.argv[4]


print('Generating Nodes: DOCUMENTS')

# Import document information from pubmed files
start_time = time.time()
with open(citations_file, 'r') as f:
    citations = dict(i.split() for i in f.readlines())
print(time.time() - start_time)
# print(citations)

# Generate the output final output file as we iterate of the part-ii file
start_time = time.time()
outCSV = open_csv(outFile)
relaCSV = open_csv(relaFile)
relaCSV.writerow(rela_header)
netOut = set()
outCSV.writerow(out_header)
e = 0
for part_ii_file in part_ii_files:
    # print('processing ', part_ii_file)
    with open( filepath(part_ii_file) , "rb" ) as dpathIn:
        for line in dpathIn.readlines():
            try:
                info = line.decode('utf-8').strip().split("\t")
                # Omit entry if either entity is missing an identifier
                if info[8] == "null" or info[9] == "null":
                    continue
                sentence_id = hash_md5( get_fields( info, id_fields, in_header ) )
                document_id = get_fields( info, ['pmid'], in_header )[0]
                document_year = citations[document_id]
                # document_info = get_fields( info, out_header[1:], in_header )
                document_out = [document_id, document_year]
                relation_out = [sentence_id, document_id]
                if document_id not in netOut:
                    outCSV.writerow( document_out )
                    netOut.add( document_id )
                if sentence_id not in netOut:
                    relaCSV.writerow( relation_out )
                    netOut.add( sentence_id )
            except KeyError:
                e = e + 1
                # print('Invalid Pubchem ID', info)
                


print('wrote', outFile.split("/")[-1], time.time() - start_time, e)
