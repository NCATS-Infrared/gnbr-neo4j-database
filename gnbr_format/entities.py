import time
import gzip
import sys
import csv
import os

# Check input and print usage if number of arguments is invalid
if len(sys.argv) != 3:
	print("Error: wrong number of arguments, check usage statement below:\n")
	print("USAGE: python GNBR_2_csv.py <path/to/part-ii-files> <path/to/outfile.csv>")
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

out_header = ['uri:ID(Entity-ID)', 'name', ':LABEL']


# Handy subroutines
def filepath( filename ):
    return import_dir+'/'+filename 

def open_csv(name, delimiter=','):
    return csv.writer(open('{}'.format(name), 'wt'), doublequote=True, delimiter=delimiter, escapechar='\\')

def get_fields(line, fields, header):
    extractor = dict( zip(header, line) )
    return [extractor[i] for i in fields]

# Assign input files to their variables
import_dir = sys.argv[1]
depPathFiles = [f for f in os.listdir(import_dir) if '-ii-' in f]
outFile = sys.argv[2]


print('Generating Nodes: ENTITY')


# Generate the output final output file as we iterate of the part-ii file
start_time = time.time()
outCSV = open_csv(outFile)
netOut = set()
outCSV.writerow(out_header)
for depPathFile in depPathFiles:
    # print('processing ' depPathFile)
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
                if "gene" in depPathFile:
                    if ":" not in info[8]:
                        info[8] = "ncbigene:" + info[8]
                    if ":" not in info[9]:
                        info[9] = "ncbigene:" + info[9]

                # Output entity 1 info if not duplicate
                subj_out = get_fields( info, ['subj_id', 'subj_name', 'subj_type'], header )
                if subj_out[0] not in netOut:
                    outCSV.writerow( subj_out )
                    netOut.add( subj_out[0] )

                # Output entity 2 info if not duplicate
                obj_out = get_fields( info, ['obj_id', 'obj_name', 'obj_type'], header )
                if obj_out[0] not in netOut:
                    outCSV.writerow( obj_out )
                    netOut.add( obj_out[0] )

            except:
                print(':( ...', info)
                raise

# print('wrote ', outFile.split("/")[-1], time.time() - start_time)