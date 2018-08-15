import os
import config
from utils import open_csv_reader, open_csv_writer
from Entities import ProcessEntity
from Sentences import ProcessSentence

def In_Sentences(source, destination):
    """
    Generate Entity file from raw GNBR flies 

    Source: Path to directory with raw GNBR files
    Destination: Path for Entity file output 

    """
    # Kalman filter (screen out duplicate rows)
    net_out = set()

    # Import header information
    in_header = config.HEADER
    out_header = config.IN_SENTENCE_HEADER

    # Open output file and write header
    writer = open_csv_writer(name=destination, fieldnames=out_header)
    writer.writerow(out_header)

    # Generate list of GNBR part ii files parocess each one
    source_files = [os.path.join(source, file) for file in os.listdir(source) if '-ii-' in file]
    for source_file in source_files:
        reader = open_csv_reader(name=source_file, fieldnames=in_header)
        try:
            # Loop through and parse rows of GNBR file
            for row in reader:
                # Get info from subject fields
                subject = ProcessEntity(
                    row_in=row, 
                    uid=config.SUBJECT_ID[0], 
                    data=config.SUBJECT_MENTION, 
                    label=config.SUBJECT_LABEL[0]
                    )
                if not subject:
                    continue

                # Get info from object fields
                object = ProcessEntity(
                    row_in=row, 
                    uid=config.OBJECT_ID[0], 
                    data=config.OBJECT_MENTION,
                    label=config.OBJECT_LABEL[0]
                    )
                if not object:
                    continue

                sentence = ProcessSentence(
                    row_in=row, 
                    uid=config.SENTENCE_ID
                    )

                subj_mention = tuple(subject + sentence)
                if subj_mention not in net_out:
                    writer.writerow(subj_mention)
                    net_out.add(subj_mention)

                obj_mention = tuple(object + sentence)
                if obj_mention not in net_out:
                    writer.writerow(obj_mention)
                    net_out.add(obj_mention)

        except Exception as e:
            print(e, row)

if __name__ == "__main__":
    import sys
    # Check input and print usage if number of arguments is invalid
    if len(sys.argv) != 3:
        print(config.CMD_LINE_ERROR)
        exit()
    In_Sentences(sys.argv[1], sys.argv[2])


"""
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
"""