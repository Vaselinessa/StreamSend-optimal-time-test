#
# Running this file as __main__ will:
# - run through the list ids contained in list_ids.csv, scheduling an email blast for each one
# 	- raw_input() provides the id for the email to be used
#		- the file at [_config.DATADIR]/list_ids.csv holds the list ids
#		- the timing for each email blast is such that they are scheduled 1 for each hour of the week, starting 1 hour after the time this module is run

import datetime
from lxml import etree
import _config
from interfaces.blast import Blast
import interfaces.utils as utils

# Returns a list of numerical strings, drawn from list_ids.csv
def _getListIds():
	f = open('%s/list_ids.csv' % _config.DATA_DIR,'r')
	data = f.read()
	f.close()
	return data.split(',')

# Creates a Blast instance, sends it to streamsend, writes id to csv
def _schedule(list_id, timestamp):
	global log, blast_ids
	blast = Blast(_config.BLAST_XML_FILE, timestamp, (list_id,))
	print >> log, blast.tostring(pretty_print=True)
	response = blast.create()
	id = utils.getId(resp)
	blast_ids.write("%s," % id)

if __name__ == '__main__' and __file__:
	import sys, os
	os.chdir(os.path.dirname(__file__))
	# get current utc time
	timestamp = datetime.datetime.utcnow()
	# open error log
	sys.err = open(_config.SYS_ERR_FILE('schedule'), 'w')
	# open blast_ids file, used for evaluating reports later !it will not be deleted or rewritten
	blast_ids = open("%s/%s.csv" % (_config.BLAST_IDS_DIR, timestamp.strftime("%Y%m%d%H%M%S")), '')
	# open blasts log, used just for diagnosis of problems if they arise
	log = open('%s/blasts-log.txt' % _config.DATA_DIR, 'w')
	print >> log, datetime.datetime.now().strftime("%A, %d %B %Y - %I:%M%p"), '\n'
	
	print 'aquiring list ids...'
	list_ids = _getListIds()
	print 'scheduling email blasts...\n\t',
	for i in range(len(list_ids)):
		print list_ids[i],
		timestamp += datetime.timedelta(hours=1)
		_schedule(list_ids[i], timestamp)
	
	print '\nCompleted.'
	# close opened files
	log.close()
	blast_ids.close()
	sys.err.close()