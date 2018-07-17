import csv
import gzip
import hashlib

def filepath( filename ):
    return import_dir+'/'+filename 

def hash_md5(array):
    return hashlib.md5( ''.join(array).encode() ).hexdigest()

def open_csv_writer(name, delimiter='\t', fieldnames=None):
    return csv.DictWriter(
    	file=gzip.open('{}'.format(name), 'wt'), 
    	delimiter=delimiter, 
    	fieldnames=fieldnames, 
    	escapechar='\\'
    	)

def open_csv_reader(name, delimiter='\t', fieldnames=None):
    return csv.DictReader(
    	gzip.open('{}'.format(name), 'rt'), 
    	delimiter=delimiter, 
    	fieldnames=fieldnames, 
    	escapechar='\\'
    	)

# def get_fields(line, fields, header):
#     extractor = dict( zip(header, line) )
#     return [extractor[i] for i in fields]


