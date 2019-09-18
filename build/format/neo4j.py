import os
import gzip
import hashlib
import pandas as pd
from collections import Counter
from build.config import HEADER

def FormatGNBR(source_dir, dest_files):
	gnbr_df = LoadGNBR(source_dir)
	gnbr_df = GenerateIDs(gnbr_df)
	gnbr_df = CleanSubjects(gnbr_df)
	gnbr_df = CleanObjects(gnbr_df)
	gnbr_df = CleanDocuments(gnbr_df)

	entities_file = dest_files['entities']
	mentions_file = dest_files['mentions']
	has_mention_file = dest_files['has_mentions']
	in_sentence_file = dest_files['in_sentences']
	EntitiesAndMentions(gnbr_df, entities_file, mentions_file, has_mention_file, in_sentence_file)

	sentences_file = dest_files['sentences']
	has_theme_file = dest_files['has_themes']
	Sentences(gnbr_df, sentences_file, has_theme_file)

	theme_file = dest_files['themes']
	Themes(gnbr_df, theme_file)

	statements_file = dest_files['statements']
	Statements(gnbr_df, statements_file)
	return



def LoadGNBR(source_dir):
	theme_files = sorted( [os.path.join(source_dir, file) for file in os.listdir(source_dir) if '-i-' in file] )
	path_files = sorted( [os.path.join(source_dir, file) for file in os.listdir(source_dir) if '-ii-' in file] )
	gnbr_df = pd.DataFrame()
	for theme_file, path_file in zip(theme_files, path_files):
	    theme_df = pd.read_csv(theme_file, compression='infer', header=0, sep='\t')
	    path_df = pd.read_csv(path_file, compression='infer', header=None, names=HEADER, sep='\t')
	    path_df = path_df.dropna(0)
	    path_df = path_df.drop_duplicates()
	    path_df.path = path_df.path.str.lower()
	    merged_df = path_df.merge(theme_df, how="inner", on=['path'])
	    gnbr_df = pd.concat([gnbr_df, merged_df], join='outer', ignore_index=True, sort=False)
	return gnbr_df

def GenerateIDs(gnbr_df):
	sentence_ids = gnbr_df['text'].copy()
	sentence_ids = sentence_ids.astype(str).str.encode('utf-8')
	sentence_ids = sentence_ids.apply(lambda x: hashlib.md5(x).hexdigest())
	gnbr_df.loc[:,'sentence_id'] = sentence_ids

	path_ids = gnbr_df['path'].astype(str)  + gnbr_df['subj_type'].astype(str) + gnbr_df['obj_type'].astype(str)
	path_ids = path_ids.astype(str).str.encode('utf-8')
	path_ids = path_ids.apply(lambda x: hashlib.md5(x).hexdigest())
	gnbr_df.loc[:,'path_id'] = path_ids
	return gnbr_df

def CleanSubjects(gnbr_df):
	uri_split = gnbr_df['subj_id'].str.split('(', expand=True)

	uris = uri_split[0]
	uris = uris.str.replace(r'^(C\d+)$', lambda m: 'MESH:' + m.group(0))
	uris = uris.str.replace(r'^(D\d+)$', lambda m: 'MESH:' + m.group(0))
	uris = uris.str.replace(r'^(\d+)$', lambda m: 'NCBIGENE:' + m.group(0))
	gnbr_df['subj_id'] = uris

	species = uri_split[1].str.strip(')')
	species = species.str.replace('Tax', 'Taxonomy')
	species = species.fillna(value="Taxonomy:9606")
	species[gnbr_df['subj_type'] != 'Gene'] = ''
	gnbr_df['subj_species'] = species
	return gnbr_df

def CleanObjects(gnbr_df):
	uri_split = gnbr_df['obj_id'].str.split('(', expand=True)

	uris = uri_split[0]
	uris = uris.str.replace(r'^(C\d+)$', lambda m: 'MESH:' + m.group(0))
	uris = uris.str.replace(r'^(D\d+)$', lambda m: 'MESH:' + m.group(0))
	uris = uris.str.replace(r'^(\d+)$', lambda m: 'NCBIGENE:' + m.group(0))
	gnbr_df['obj_id'] = uris

	species = uri_split[1].str.strip(')')
	species = species.str.replace('Tax', 'Taxonomy')
	species = species.fillna(value="Taxonomy:9606")
	species[gnbr_df['obj_type'] != 'Gene'] = ''
	gnbr_df['obj_species'] = species
	return gnbr_df

def CleanDocuments(gnbr_df):
	pmids = gnbr_df['pmid'].astype(str)
	pmids = pmids.str.replace(r'^(\d+)$', lambda m: 'PUBMED:' + m.group(0))
	gnbr_df['pmid'] = pmids
	return gnbr_df

def EntitiesAndMentions(gnbr_df, entities_file, mentions_file, has_mention_file, in_sentence_file):
	subj_df = gnbr_df[['subj_name', 'subj_name_raw','subj_id', 'subj_species', 'subj_type', 'sentence_id']]
	subj_df.columns = ['name' , 'mention', 'uri', 'species', 'type', 'sentence_id']
	obj_df = gnbr_df[['obj_name', 'obj_name_raw','obj_id', 'obj_species', 'obj_type', 'sentence_id']]
	obj_df.columns = ['name', 'mention', 'uri', 'species', 'type', 'sentence_id']
	concepts = pd.concat([subj_df, obj_df], ignore_index = True)

	WriteEntities(concepts, entities_file)
	WriteMentions(concepts, mentions_file)
	WriteHasMentions(concepts, has_mention_file)
	WriteInSentence(concepts, in_sentence_file)
	return

def WriteEntities(concepts, entities_file):
	entities = concepts[['mention', 'uri', 'type', 'species']]
	entities = entities.groupby(by=['uri','type', 'species'])['mention'].apply(lambda x: x.values.tolist())
	entities = entities.apply(lambda x: Counter(x).most_common(1)[0][0])
	entities = pd.DataFrame(entities)
	entities.reset_index(inplace=True)
	entities = entities.drop_duplicates(subset=['uri'] ,keep ='last')
	print('Writing nodes file %s' % entities_file)
	entities.to_csv(entities_file, 
	                columns=["uri", "type", "mention", 'species'], 
	                header=['uri:ID(Entity-ID)', 'type:LABEL', 'name', 'species'], 
	                index=False, compression='gzip')
	return 

def WriteMentions(concepts, mentions_file):
	mentions = concepts[['name','mention']]
	mentions = mentions.drop_duplicates()
	print('Writing nodes file: %s' % mentions_file)
	mentions.to_csv(mentions_file, 
	                columns=["name", "mention"], 
	                header=['formatted', 'mention:ID(Mention-ID)'], 
	                index=False, compression='gzip')
	return

def WriteHasMentions(concepts, has_mention_file):
	has_mention = concepts[['mention', 'uri']]
	has_mention = has_mention.drop_duplicates()
	print('Writing edges file: %s' % has_mention_file)
	has_mention.to_csv(has_mention_file, 
	                columns=["uri", "mention"], 
	                header=[':START_ID(Entity-ID)', ':END_ID(Mention-ID)'], 
	                index=False, compression='gzip')
	return

def WriteInSentence(concepts, in_sentence_file):
	in_sentence = concepts[['uri','mention','sentence_id']]
	in_sentence = in_sentence.drop_duplicates()
	print('Writing edges file: %s' % in_sentence_file)
	in_sentence.to_csv(in_sentence_file, 
	                   columns=["uri", "mention", "sentence_id"], 
	                   header=[":START_ID(Entity-ID)", "etext", ":END_ID(Sentence-ID)"], 
	                   index=False, compression='gzip')
	return


def Sentences(gnbr_df, sentences_file, has_theme_file):
	sentence_df = gnbr_df[['subj_id', 'obj_id', 'text', 'pmid', 'path', 'sentence_id', 'path_id']]
	sentences = sentence_df[['sentence_id', 'text', 'pmid']]
	sentences = sentences.drop_duplicates(subset='sentence_id')
	print('Writing nodes file: %s' % sentences_file)
	sentences.to_csv(sentences_file, 
	                columns=["sentence_id", "text", "pmid"], 
	                header=[":ID(Sentence-ID)", "text", "pmid"], 
	                index=False, compression='gzip')
	has_theme = sentence_df[['sentence_id', 'path', 'path_id']]
	has_theme['entities'] = sentence_df['subj_id'].astype(str) + ';' + sentence_df['obj_id'].astype(str)
	has_theme = has_theme.drop_duplicates()
	print('Writing edges file: %s' % has_theme_file)
	has_theme.to_csv(has_theme_file, 
	                 columns=["sentence_id", "path", "path_id", "entities"], 
	                 header=[":START_ID(Sentence-ID)", "path", ":END_ID(Path-ID)", "entities:string[]"], 
	                 index=False, compression='gzip')
	return

def Themes(gnbr_df, themes_file):
	themes_df = gnbr_df.select_dtypes(include='float64')
	themes_df = themes_df[[i for i in themes_df.columns if not i.endswith('.ind')]]
	themes_df = themes_df.rank(numeric_only=True, pct=True, method='dense')
	themes_df = themes_df.fillna(0) 
	themes_df.columns = [i + ':float' for i in themes_df.columns]
	themes_df[':ID(Path-ID)'] = gnbr_df['path_id']
	themes_df = themes_df.drop_duplicates()
	print('Writing nodes file: %s' %themes_file)
	themes_df.to_csv(themes_file, index=False, compression='gzip')
	return

def Statements(gnbr_df, statements_file):
	statements = gnbr_df.groupby(by=['subj_id','obj_id']).sum(numeric_only=True)
	statements = statements.drop(['loc'], axis=1)
	statements = statements.select_dtypes(include='float64')
	statements = statements[[i for i in statements.columns if not i.endswith('.ind')]]
	statements = statements.rank(numeric_only=True, pct=True, method='dense')
	# statements = statements[statements > 0.05].dropna(how='all')
	statements.columns = [i + ':float' for i in statements.columns]
	statements = pd.DataFrame(statements)
	statements.reset_index(inplace=True)
	statements = statements.fillna(0) 
	statements = statements.rename(columns = {'subj_id': ':START_ID(Entity-ID)', 'obj_id': ':END_ID(Entity-ID)'})
	print('Writing edges file: %s' % statements_file)
	statements.to_csv(statements_file, index=False, compression='gzip')
	return
