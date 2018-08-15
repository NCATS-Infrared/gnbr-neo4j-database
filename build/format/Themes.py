import os
import config
from utils import csv_reader, open_csv_writer, open_csv_reader, hash_md5



def ProcessThemes(theme_file):
    path_to_theme = dict()
    themes = csv_reader( theme_file )
    dynamic_header = next(themes)
    dynamic_header = [x.lower().replace(" ", "_").replace('.ind', '_ind') + ':int' for x in dynamic_header][1:]
    path_to_theme["header"] = config.THEME_HEADER + dynamic_header
    for line in themes:
        path_to_theme[line[0].lower()] = list( map(float, line[1:]) )

    return path_to_theme

def ProcessPath(row_in, uid=[], data=[], label=[]):
    """
    Parse row of raw GNBR file and return row of neo4j Theme node file.

    Row_in: Row from a csv DictReader 
    uid: Field(s) for unique id
    label: Field(s) for node label
    data:  Fields with node data

    Return: list with row info (empty if row has a null uri)
    """
    if row_in['subj_id'] != "null" and row_in['obj_id'] != "null":
        # Generate uid from path and label fields
        path = [row_in[field].lower() for field in uid]
        labels = sorted( [row_in[field] for field in label] )
        uri = hash_md5(path + labels)

        # Generate label string
        labels = '|'.join(labels)

        # Generate output row 
        row_out = [uri, labels] + list( map(int, data) )
    else:
        row_out = []
    return row_out


def Themes(source, destination):

    # We loop over all pairs of corresponding part i (theme) and ii (path) files so need to sort
    theme_files = sorted( [os.path.join(source, file) for file in os.listdir(source) if '-i-' in file] )
    path_files = sorted( [os.path.join(source, file) for file in os.listdir(source) if '-ii-' in file] )

    # Generate output filename for each pair 
    out_files = [destination.replace('.csv', '_%i.csv'%idx) for idx in range(len(theme_files))]

    # Loop over corresponding theme, path, and output file triples
    for theme_file, path_file, out_file in zip(theme_files, path_files , out_files):
        net_out = set()

        # Get dictionary linking paths to their theme distributions
        paths_to_themes = ProcessThemes( theme_file )

        # Open output file and write header
        writer = open_csv_writer( out_file )
        writer.writerow(paths_to_themes["header"])

        # Open path file and loop through
        reader = open_csv_reader(path_file, fieldnames=config.HEADER)
        for row in reader:

            # Process each path and output
            theme = ProcessPath(
                row_in=row,
                uid=config.THEME_ID,
                label=config.THEME_LABEL,
                data=paths_to_themes[row['path'].lower()]
                )
            if theme:
                if theme[0] not in net_out:
                    writer.writerow( theme )
                    net_out.add(theme[0])

if __name__ == "__main__":
    import sys
    # Check input and print usage if number of arguments is invalid
    if len(sys.argv) != 3:
        print(config.CMD_LINE_ERROR)
        exit()
    Themes(sys.argv[1], sys.argv[2])
