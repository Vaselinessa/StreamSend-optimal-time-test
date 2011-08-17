LOGIN_ID													= '' # Get this from Streamsend website
API_KEY														= '' # Get this from Streamsend website
DATA_DIR													=	'data'
DIR_OF_USER_LISTS									= '%s/168-user-lists' % DATA_DIR
SUBSCRIBERS_FILE 									= '%s/My Subscribers.txt' % DATA_DIR
IGNORE_FIRST_LINE_OF_SUBSCRIBERS 	= True # first line of subscribers file defaults to contain fields names
BLAST_XML_FILE										= '%s/blast.xml' % DATA_DIR
BLAST_IDS_DIR											= '%s/blast-ids' % DATA_DIR
ANALYSIS_DIR											= '%s/analysis' % DATA_DIR
ERRLOG_SETUP											= 'data/errlog-setup.txt'
ERRLOG_SCHEDULE										= 'data/errlog-schedule.txt'
ERRLOG_CLEANUP										= 'data/errlog-cleanup.txt'
ERRLOG_ANALYZE										= 'data/errlog-analyze.txt'

def SYS_ERR_FILE(name): 					return '%s/errlog-%s.txt' % (DATA_DIR, name)

# ensure subdirectories exist
import os
def _ensureDirectory(rel_path):
	path = os.path.join(os.path.dirname(__file__), rel_path);
	if not os.path.exists(path): os.mkdir(path)

for x in DATA_DIR, DIR_OF_USER_LISTS, BLAST_IDS_DIR, ANALYSIS_DIR: _ensureDirectory(x)