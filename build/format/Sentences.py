from utils import hash_md5, open_csv_reader, open_csv_writer
import config
import os

def ProcessSentence(row_in, uid=[], data=[]):
    """
    Parse row of raw GNBR file and return row of neo4j Sentence node file.

    Row_in: Row from a csv DictReader 
    uid: Field(s) for unique id
    label: Field(s) for node label
    data:  Fields with node data

    Return: list with row info (empty if row has a null uri)
    """

    # Check for valid row
    if row_in['subj_id'] != "null" and row_in['obj_id'] != "null":
        # Generate uid using md5 hash of id fields
        uri = hash_md5( [row_in[field] for field in uid] )
        # Get output row info and prepend with uid
        row_out = [row_in[field] for field in data]
        row_out = [uri] + row_out
    else:
        row_out = []
    return row_out

def Sentences(source=None, destination=None):
    """
    Generate neo4j Sentences node file from raw GNBR flies 

    Source: Path to directory with raw GNBR files
    Destination: Path for Sentences file output 

    """

    # Kalman filter (screen out duplicate rows)
    net_out = set()

    # Import header information
    in_header = config.HEADER
    out_header = config.SENTENCE_HEADER

    # Open output file and write header
    writer = open_csv_writer(name=destination, fieldnames=out_header)
    writer.writerow(out_header)

    # Generate list of GNBR part ii files
    source_files = [os.path.join(source, file) for file in os.listdir(source) if '-ii-' in file]

    # Loop through GNBR files
    for source_file in source_files:

        # Open GNBR file and loop through and parse rows
        reader = open_csv_reader(name=source_file, fieldnames=in_header)
        for row in reader:
            sentence = ProcessSentence(
                row_in=row, 
                uid=config.SENTENCE_ID, 
                data=config.SENTENCE_INFO
                )

            # Check for null or duplicate, and write row if all G.
            if sentence:
                if sentence[0] not in net_out:
                    writer.writerow( sentence )
                    net_out.add(sentence[0])

if __name__ == "__main__":
    import sys
    # Check input and print usage if number of arguments is invalid
    if len(sys.argv) != 3:
        print(config.CMD_LINE_ERROR)
        exit()

    # Run on command line arguments
    Sentences(sys.argv[1], sys.argv[2])


