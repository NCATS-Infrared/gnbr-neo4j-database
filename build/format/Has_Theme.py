import os
import config
from Sentences import ProcessSentence
from Themes import ProcessPath
from utils import open_csv_reader, open_csv_writer

def Has_Themes(source, destination):
    """
    Generate Entity file from raw GNBR flies 

    Source: Path to directory with raw GNBR files
    Destination: Path for Entity file output 

    """
    # Kalman filter (screen out duplicate rows)
    net_out = set()

    # Import header information
    in_header = config.HEADER
    out_header = config.HAS_THEME_HEADER

    # Open output file and write header
    writer = open_csv_writer(name=destination, fieldnames=out_header)
    writer.writerow(out_header)

    # Generate list of GNBR part ii files parocess each one
    source_files = [os.path.join(source, file) for file in os.listdir(source) if '-ii-' in file]
    for source_file in source_files:
        reader = open_csv_reader(name=source_file, fieldnames=in_header)
        for row in reader:
            # Get info from subject fields

            sentence = ProcessSentence(
                row_in=row, 
                uid=config.SENTENCE_ID
                )
            if not sentence:
                continue

            theme = ProcessPath(
                row_in=row,
                uid=config.THEME_ID,
                label=config.THEME_LABEL
                )
            path = row['path'].lower()
            out = tuple( sentence + theme[:1] )
            if out not in net_out:
                writer.writerow(out + tuple([path]))
                net_out.add(out)

if __name__ == "__main__":
    import sys
    # Check input and print usage if number of arguments is invalid
    if len(sys.argv) != 3:
        print(config.CMD_LINE_ERROR)
        exit()
    Has_Themes(sys.argv[1], sys.argv[2])
"""
# Check input and print usage if number of arguments is invalid
if len(sys.argv) != 3:
	print("Error: wrong number of arguments, check usage statement below:\n")
	print("USAGE: python GNBR_2_csv.py <path/to/part-ii-files> <path/to/outfile.csv>")
	exit()


# Define input and output headers
header = [
    "pmid", "loc", 
    "subj_name", "subj_loc", 
    "obj_name", "obj_loc",
    "subj_name_raw", "obj_name_raw", 
    "subj_id", "obj_id", 
    "subj_type", "obj_type", 
    "path", "text"
    ] 
out_header = [':START_ID(Sentence-ID)',':END_ID(Path-ID)', 'dpath']

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

print('Generating Relationships: HAS_PREDICATE')

# Open output file and write header
start_time = time.time()
outCSV = open_csv(outFile)  
netOut = set()
outCSV.writerow(out_header)

# Loop over input files and stream output
for depPathFile in depPathFiles:
    # print('processing', depPathFile)
    with open( filepath(depPathFile) , "rb" ) as dpathIn:
        for line in dpathIn.readlines():
            try:
                info = line.decode('utf-8').strip().split("\t")
                # Omit entry if either entity is missing an identifier
                if info[8] == "null" or info[9] == "null":
                    continue

                # Normalize path because different cases in part i and part ii
                info[-2] = info[-2].lower()
                path = info[-2]

                # Use md5 hashes of path|type1|type2 and sentence text as ids  
                types = sorted(get_fields(info, ['subj_type', 'obj_type'], header))
                path = get_fields(info, ['path'], header)
                path_id = hash_md5( path + types )
                sentence_id = hash_md5( get_fields( info, ['text'], header ) )

                # Output sentence_id and path_id
                out = tuple( [sentence_id, path_id] )
                if out not in netOut:
                    outCSV.writerow(out + tuple(path))
                    netOut.add(out)
            except:
                print(':( ...', info)
                raise

    # print("finished processing ", depPathFile, time.time() - start_time)

print('wrote', outFile.split('/')[-1], time.time() - start_time)
"""