#!/usr/bin/python3
from format.Entities import Entities
from format.InSentences import InSentences
from format.Sentences import Sentences
from format.AboutThemes import AboutThemes
from format.Themes import Themes
# from format.InDocuments import InDocuments
# from format.Documents import Documents

from download.ThreadedDownload import ThreadedDownload
from format.Sentences import Sentences
from format.Statements import Statements

import config
import os.path
import sys


URLS=config.URLS
DWNLD_DIR=os.path.expanduser(config.DWNLD_DIR)
NEO_DATA_DIR=os.path.expanduser(config.NEO_DATA_DIR)
HEADER = config.HEADER

if __name__ == "__main__":

	downloader = ThreadedDownload(
		urls=URLS, 
		destination=DWNLD_DIR, 
		directory_structure=False, 
		thread_count=5, 
		url_tries=3
		)  
	print 'Downloading %s files' % len(URLS)
	downloader.run()
	print 'Downloaded %(success)s of %(total)s' % {'success': len(downloader.report['success']), 'total': len(URLS)}

	if len(downloader.report['failure']) > 0:
		print '\nFailed urls:'
		for url in downloader.report['failure']:
			print url
		sys.exit()

	# Generate node files
	print('Generating Nodes: ENTITY')
	Entities(files_dir=DWNLD_DIR, destination=NEO_DATA_DIR + "/entities.csv.gz")

	if config.MINI == False:
		print('Generating Nodes: SENTENCE')
		Sentences(files_dir=DWNLD_DIR, destination=NEO_DATA_DIR + "/sentences.csv.gz")

		print('Generating Nodes: THEME')
		Themes(files_dir=DWNLD_DIR, destination=NEO_DATA_DIR + "/themes.csv.gz")

	Generate relationship files
	print('Generating Relationships: STATEMENT')
	Statements(files_dir=DWNLD_DIR, destination=NEO_DATA_DIR + "/statements.csv.gz")

	if config.MINI == False:
		print('Generating Relationships: IN SENTENCE')
		In_Sentences(files_dir=DWNLD_DIR, destination=NEO_DATA_DIR + "/in_sentences.csv.gz")

		print('Generating Relationships: HAS THEME')
		Has_Themes(files_dir=DWNLD_DIR, destination=NEO_DATA_DIR + "/has_themes.csv.gz")

