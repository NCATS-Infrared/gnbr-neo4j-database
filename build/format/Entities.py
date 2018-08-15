import os
import config
from utils import open_csv_reader, open_csv_writer


# Function for 
def ProcessEntity(row_in, uid=[], data=[], label=[]):
    """
    Parse row of raw GNBR file and return row of neo4j Entity node file.

    Row_in: Row from a csv DictReader 
    uid: Field(s) for unique id
    label: Field(s) for node label
    data:  Fields with node data

    Return: list with row info (empty if row has a null uri)
    """
    if row_in['subj_id'] != "null" and row_in['obj_id'] != "null":
        # Get output row
        row_out = [row_in[field] for field in data]

        # If Gene strip tax id and add uri prefix
        if row_in[label] == 'Gene':
            uri = row_in[uid].split("(")[0]
            uri = "ncbigene:" + uri
            row_out[0] = uri

        # Add curie prefix to Chemical or Diseases if missing
        elif ":" not in row_in[uid]:
            uri = "MESH:" + row_in[uid]
            row_out[0] = uri
        else: 
            pass
    else:
        row_out = []
    return row_out


# Script for generating entity nodes.  
def Entities(source, destination):
    """
    Generate Entity file from raw GNBR flies 

    Source: Path to directory with raw GNBR files
    Destination: Path for Entity file output 

    """
    # Kalman filter (screen out duplicate rows)
    net_out = set()

    # Import header information
    in_header = config.HEADER
    out_header = config.ENTITY_HEADER

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
                    data=config.SUBJECT_INFO, 
                    label=config.SUBJECT_LABEL[0]
                    )
                # Check for null or duplicate, and write row if all G.
                if subject:
                    if subject[0] not in net_out:
                        writer.writerow( subject )
                        net_out.add(subject[0])

                # Get info from object fields
                object = ProcessEntity(
                    row_in=row, 
                    uid=config.OBJECT_ID[0], 
                    data=config.OBJECT_INFO,
                    label=config.OBJECT_LABEL[0]
                    )
                # Check for null or duplicate, and write row if all G.
                if object:
                    if object[0] not in net_out:
                        writer.writerow( object )
                        net_out.add(object[0])
        except Exception as e:
            print(e, row)


if __name__ == "__main__":
    import sys
    # Check input and print usage if number of arguments is invalid
    if len(sys.argv) != 3:
        print(config.CMD_LINE_ERROR)
        exit()
    Entities(sys.argv[1], sys.argv[2])