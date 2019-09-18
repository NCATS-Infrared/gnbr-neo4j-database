#!/usr/bin/python3


import os.path
import errno
import sys

from build.config import URLS, DWNLD_DIR, NEO_DATA_DIR, FILES
from build.download.ThreadedDownload import ThreadedDownload
from build.format.neo4j import FormatGNBR


URLS=URLS
DWNLD_DIR=os.path.expanduser(DWNLD_DIR)
NEO_DATA_DIR=os.path.expanduser(NEO_DATA_DIR)
OUT_FILES = {k: os.path.join(NEO_DATA_DIR, v) for k, v in FILES.items()}
if __name__ == "__main__":
    try:
        os.makedirs(DWNLD_DIR)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass


    downloader = ThreadedDownload(
        urls=URLS, 
        destination=DWNLD_DIR, 
        directory_structure=False, 
        thread_count=5, 
        url_tries=3
        )  
    print('Downloading %s files' % len(URLS) )
    downloader.run()
    print('Downloaded %(success)s of %(total)s' % {'success': len(downloader.report['success']), 'total': len(URLS)})

    if len(downloader.report['failure']) > 0:
        print('\nFailed urls:')
        for url in downloader.report['failure']:
            print(url)
        sys.exit()

    try:
        os.makedirs(NEO_DATA_DIR)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass

    FormatGNBR(DWNLD_DIR, OUT_FILES)

