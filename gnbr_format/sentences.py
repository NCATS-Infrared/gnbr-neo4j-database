from utils import open_csv_reader, open_csv_writer
import config
import time
import sys
import os


def format_sentences(part_ii_file, outfile):
    in_header = config.HEADER
    out_header = config.SENTENCE_HEADER
    id_fields = config.SENTENCE_ID 
    outCSV = open_csv_writer(outFile, header=out_header)
    with open_csv_reader(part_ii_file), open_csv_writer(outFile, header=out_header) as reader, writer:
        netOut = set()
        writer.writeheader()
        for row in reader:
            if row['subj_id'] == "null" or info['obj_id'] == "null":
                continue
            sentence_id = hash_md5( [row[field] for field in id_fields] )
            sentence_info = [row[field] for field in out_header[1:]]
            sentence_out = [sentence_id] + sentence_info
            if sentence_id not in netOut:
                outCSV.writerow( {i:j for i,j in zip(out_header, sentence_out)} )
                netOut.add( sentence_id )

if __name__ == main:
    # Check input and print usage if number of arguments is invalid
    if len(sys.argv) != 3:
        print(config.CMD_LINE_ERROR)
        exit()

    import_dir = sys.argv[1]
    part_ii_files = [f for f in os.listdir(import_dir) if '-ii-' in f]
    outFile = sys.argv[2] + sentences.txt.gz
    for file in part_ii_files:
        format_sentences(file, outFile)
