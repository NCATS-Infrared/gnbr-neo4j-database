import csv
import gzip
import hashlib


def hash_md5(array):
    return hashlib.md5( ''.join(array).encode() ).hexdigest()

def open_csv_writer(name, delimiter='\t', fieldnames=None):
    # return csv.writer(file=gzip.open('{}'.format(name), 'wt'), delimiter=delimiter, fieldnames=fieldnames)
    return csv.writer(gzip.open('{}'.format(name), 'wt'), delimiter=delimiter)


def open_csv_reader(name, delimiter='\t', fieldnames=None):
    return csv.DictReader(
    	(x.replace('\0', '') for x in gzip.open('{}'.format(name), 'rt', encoding='utf-8', newline='')), 
    	delimiter=delimiter, 
    	fieldnames=fieldnames
    	# escapechar='\\'
    	)

def csv_reader(name, delimiter='\t'):
    return csv.reader(
        (x.replace('\0', '') for x in gzip.open('{}'.format(name), 'rt', encoding='utf-8', newline='')), 
        delimiter=delimiter
        )


def ProcessSentence(row_in, uid=[], data=[], label=[], in_header=None, out_header=None):
    uid = hash_md5( [row_in[field] for field in uid] )
    label = [row_in[field] for field in label]
    if row_in['subj_id'] != "null" and row_in['obj_id'] != "null":
        # Strip tax id from genes and store separately
        # if "(Tax:" in row_in['subj_id']:
        #     temp = row_in['subj_id'].split("(")
        #     row_in['subj_id'] = temp[0]
        # if "(Tax:" in row_in[obj_id]:
        #     temp = row_in[obj_id].split("(")
        #     row_in[obj_id] = temp[0]
        # if ":" not in row_in[obj_id]:
        #     row_in[obj_id] = "ncbigene:" + row_in[obj_id]
        # if ":" not in row_in[subj_id]:
        #     row_in[subj_id] = "ncbigene:" + row_in[subj_id]
        
        row_in = [row_in[field] for field in data]
        row_out = [uid] + label + row_in
        # row_out = {i:j for i,j in zip(out_header, row_out)}

    else:
        row_out = []
    return row_out
    # return {'uid': uid, 'row': row_out}


