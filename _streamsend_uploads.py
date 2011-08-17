#
# Called by 'setup.py'
# Executes an upload for each file in _config.DIR_OF_USER_LISTS

import glob, sys, os
import _config
import interfaces.upload as upload
import interfaces.utils as utils

def run():
	upload_ids = []
	files = glob.iglob("%s/*.txt" % _config.DIR_OF_USER_LISTS)
	for file in files:
		httpresp = upload.create(file)
		try:
			id = utils.getId(httpresp)
			upload_ids.append(id)
			fileNumber = os.path.splitext(os.path.basename(file))[0]
			print ("{%s:%s} " % (fileNumber, id)),
		except Exception as (msg):
			print >> sys.err, 'Exception at _streamsend_uploads.py#run() - line 16-19'
			print >> sys.err, '\t', msg
	print
	return upload_ids
		

		
	