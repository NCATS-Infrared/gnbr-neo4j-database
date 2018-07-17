import time
import hashlib
import gzip
import sys
import csv
import os

# Define input header.  Output header generated dynamically.
header = [
    "pmid", "loc", 
    "subj_name", "subj_loc", 
    "obj_name", "obj_loc",
    "subj_name_raw", "obj_name_raw", 
    "subj_id", "obj_id", 
    "subj_type", "obj_type", 
    "path", "text"
    ]

# out_header = [':ID(Path-ID)', ':LABEL', 'path']
out_header = [':ID(Path-ID)', ':LABEL']
id_fields = ['path']
label_fields = ['subj_type', 'obj_type']

# Check input and print usage if number of arguments is invalid
if len(sys.argv) != 3:
	print("Error: wrong number of arguments, check usage statement below:\n")
	print("USAGE: python GNBR_2_csv.py <path/to/part-i-files> <path/to/flattened-graph-outfile.csv>")
	exit()

# Handy helper functions
def filepath( filename ):
    return import_dir+'/'+filename 

def open_csv(name, delimiter=','):
    return csv.writer(open('{}'.format(name), 'wt'), doublequote=True, delimiter=delimiter, escapechar='\\')

def hash_md5(array):
    return hashlib.md5( ''.join(array).encode() ).hexdigest()

def get_fields(line, fields, header):
    extractor = dict( zip(header, line) )
    return [extractor[i] for i in fields]

# Assign input files to their variables.
import_dir = sys.argv[1]
outName = sys.argv[2].replace('.csv', '')

# We loop over all pairs of corresponding part i and ii files so need to sort
themeFiles = sorted([f for f in os.listdir(import_dir) if '-i-' in f])
depPathFiles = sorted([f for f in os.listdir(import_dir) if '-ii-' in f])

# Generate output filename for each pair 
outFiles = [outName + '_%i.csv' %i  for i in range(len(themeFiles))]


print('Generating Nodes: PREDICATE')


# Create a dictionary of the dependency paths (key) and their theme score vectors (value)
start_time = time.time()
for themeFile, depPathFile, outFile in zip(themeFiles, depPathFiles , outFiles):
    depDict = dict()
    with open( filepath(themeFile), "rb") as themeIn:
        depDict["header"] = themeIn.readline().decode('utf-8').strip().split("\t")
        for line in themeIn.readlines():
            info = line.decode('utf-8').strip().split("\t")
            depDict[info[0]] = map(float, info[1:])

    # Dynamically create output header for neo4j import.
    dynamic_header = [x.lower().replace(" ", "_").replace('.ind', '_ind') + ':int' for x in depDict["header"]][1:]
    outThemeHeader = out_header + dynamic_header

    # Generate the output final output file as we iterate of the part-ii file
    outCSV = open_csv(outFile)
    netOut = set()
    outCSV.writerow(outThemeHeader)
    with open( filepath(depPathFile) , "rb") as dpathIn:
        i = 0
        for line in dpathIn.readlines():
            try:
                info = line.decode('utf-8').strip().split("\t")
                # Omit entry if either entity is missing an identifier
                if info[8] == "null" or info[9] == "null":
                    continue
 
                # Noramlize dependency path case.  Change in place for later use.
                info[-2] = info[-2].lower()
                dpKey = info[-2]

                # Check if dependency graphs match across part i and ii files.
                if dpKey in depDict.keys():

                    # Use md5 hashes of path|type1|type2 unique id
                    labels = sorted( get_fields(info, label_fields, header) )
                    path_id = hash_md5( get_fields(info, id_fields, header) + labels )

                    # Check if duplicate id and output id, label, path, and distribution. 
                    if path_id not in netOut:
                        info_out = list( map(int, depDict.get(dpKey)) )
                        label = '|'.join(labels)
                        # outCSV.writerow( [path_id, label, dpKey] + info_out )
                        outCSV.writerow( [path_id, label] + info_out ) 
                        netOut.add( path_id )
                else:
                    print("ERROR: MISSING ENTRY")

            except:
                print(':( ...', info)
                raise
    # print("finished processing ", themeFile, depPathFile, time.time() - start_time)
    # print('wrote', outFile.split('/')[-1], time.time() - start_time)
