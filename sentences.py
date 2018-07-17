import time
import gzip
import hashlib
import sys
import csv
import os

# Check input and print usage if number of arguments is invalid
if len(sys.argv) != 3:
	print("Error: wrong number of arguments, check usage statement below:\n")
	print("USAGE: python GNBR_2_csv.py <path/to/part-ii-files/> <path/to/outfile.csv.gz>")
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

out_header = [':ID(Sentence-ID)', 'pmid', 'loc', 'text']
id_fields = ['text']


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
part_ii_files = [f for f in os.listdir(import_dir) if '-ii-' in f]
outFile = sys.argv[2]


print('Generating Nodes: SENTENCE')

# Generate the output final output file as we iterate of the part-ii file
start_time = time.time()
outCSV = open_csv(outFile)
netOut = set()
outCSV.writerow(out_header)
for part_ii_file in part_ii_files:
    # print('processing ', part_ii_file)
    with open( filepath(part_ii_file) , "rb" ) as dpathIn:
        i = 0
        for line in dpathIn.readlines():
            try:
                info = line.decode('utf-8').strip().split("\t")
                # Omit entry if either entity is missing an identifier
                if info[8] == "null" or info[9] == "null":
                    continue
                sentence_id = hash_md5( get_fields( info, id_fields, in_header ) )
                sentence_info = get_fields( info, out_header[1:], in_header )
                sentence_out = [sentence_id] + sentence_info
                if sentence_id not in netOut:
                    outCSV.writerow( sentence_out )
                    netOut.add( sentence_id )
            except:
                print(':( ...', info)
                raise


# print('wrote', outFile.split("/")[-1], time.time() - start_time)