import time
import hashlib
# from utils import *
import gzip
import sys
import csv
import os

# Check input and print usage if number of arguments is invalid
if len(sys.argv) != 3:
	print("Error: wrong number of arguments, check usage statement below:\n")
	print("USAGE: python GNBR_2_csv.py <path/to/part-ii-files/> <path/to/outfile.csv>")
	exit()

# Define input and output headers.
header = [
    "pmid", "loc", 
    "subj_name", "subj_loc", 
    "obj_name", "obj_loc",
    "subj_name_raw", "obj_name_raw", 
    "subj_id", "obj_id", 
    "subj_type", "obj_type", 
    "path", "text"
    ] 
out_header = [':START_ID(Entity-ID)','raw_string', ':END_ID(Sentence-ID)']

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
depPathFiles = [f for f in os.listdir(import_dir) if '-ii-' in f]
outFile = sys.argv[2]
print('Generating Relationships: IN_SENTENCE')
# Generate the output final output file as we iterate of the part-ii file
start_time = time.time()
outCSV = open_csv(outFile)
netOut = set()
outCSV.writerow(out_header)
for depPathFile in depPathFiles:
    # print('processing', depPathFile)
    with open( filepath(depPathFile) , "rb" ) as dpathIn:
        i = 0
        for line in dpathIn.readlines():
            try:
                info = line.decode('utf-8').strip().split("\t")
                # Omit entry if either entity is missing an identifier
                if info[8] == "null" or info[9] == "null":
                    continue
                # Strip tax id from genes and store separately
                if "(Tax:" in info[9]:
                    temp = info[9].split("(")
                    info[9] = temp[0]
                    species = temp[1].strip("Tax:").strip(")")
                if "(Tax:" in info[8]:
                    temp = info[8].split("(")
                    info[8] = temp[0]
                    species = temp[1].strip("Tax:").strip(")")   
                else:
                    species = "9606"

                # Add curie stem to genes
                if "gene" in depPathFile:
                    if ":" not in info[8]:
                        info[8] = "ncbigene:" + info[8]
                    if ":" not in info[9]:
                        info[9] = "ncbigene:" + info[9]

                # Use md5 hash of sentence as unique id
                sentence_id = hash_md5( get_fields( info, ['text'], header ) )

                # Output entity_id, sentence_id for entity 1
                subj_id = get_fields( info, ['subj_id', 'subj_name_raw'], header )
                subj_out = tuple( subj_id + [sentence_id] ) 
                if subj_out not in netOut:
                    outCSV.writerow( subj_out )
                    netOut.add( subj_out )

                # Output entity_id, sentence_id for entity 2
                obj_id = get_fields( info, ['obj_id', 'obj_name_raw'], header )
                obj_out = tuple( obj_id + [sentence_id] )
                if obj_out not in netOut:
                    outCSV.writerow( obj_out )
                    netOut.add( obj_out )
            except:
                print(':( ...', info)
                raise

print('wrote', outFile.split('/')[-1], time.time() - start_time)
