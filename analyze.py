#!/usr/bin/python

import os, sys, datetime
from lxml import etree
import _config, interfaces.ss_views, interfaces.blast, interfaces.connection

def test_index():
	global results
	results = index(14205017)
	print len(results)
	
def get_blast_ids(fname_sans_ext):
	fpath = "%s/%s.csv" % (_config.BLAST_IDS_DIR, fname_sans_ext)
	f = open(fpath)
	ids = f.read().split(',')
	f.close()
	return ids
	
# Returns [[id, [<Element view>, <Element view>,...]],...]
def get_views_from_api(blast_ids):
	results = [] # list of tuples: (blast_id, views); 'views' is list of instances of interfaces/connect.Element
	for id in blast_ids:
		if len(id) > 0:
			print id,
			response = interfaces.ss_views.index(id)
			if response.status == 200:
				tree = etree.fromstring(response.read())
				views = tuple(interfaces.ss_views.View(x) for x in tree.xpath('//view'))
				results.append([id, views])
	print
	return results

# Get day and time of each blast
# Expects list [lxml obj]
def parse_results(results):
	outputs = []
	for r in results:
		first = r[0]
		id = int(r[0])
		views = r[1] if type(r[1]) in (int,str) else len(r[1])
		print 'Getting blast #%d' % id
		resp = interfaces.blast.show(id)
		if resp.status == 200:
			tree = etree.fromstring(resp.read())
			timestamp = tree.xpath('//scheduled-for')[0].text
			dt = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
			output = id, dt, views
			outputs.append(output)
		else:
			print >> sys.stderr, 'Error requesting Blast #%d' % int(r[0])
	return outputs
	
# 'results' is list of tuple (blast-id, [view, view...])
def log_results(results, fname_sans_ext):
	fpath = "%s/%s-views.txt" % (_config.ANALYSIS_DIR, fname_sans_ext)
	f = open(fpath, 'w')
	for r in results:
		print r[0],
		blast 	= interfaces.blast.Response.forId(r[0])
		views		= len(r[1])
		print >> f, blast.id, blast.datetime().strftime("%a %I:%M%p"), views
	print
	f.close()
	
if __name__ == '__main__':
	# move to this dir, open error log
	os.chdir(os.path.dirname(__file__))
	sys.stderr = open(_config.ERRLOG_ANALYZE, 'w')
	fname = raw_input('blast_ids csv filename (no path, no ext)?: ')
	print 'getting ids from file...'
	ids = get_blast_ids(fname)
	print 'getting views from api...'
	views_list = get_views_from_api(ids)
	views_list.sort(key=lambda x: -len(x[1]))
	print '%d results' % len(views_list)
	print 'logging top results...'
	log_results(views_list, fname)
	print 'Completed.'
	sys.stderr.close()
	
