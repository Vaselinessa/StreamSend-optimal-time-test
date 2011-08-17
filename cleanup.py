#
# Run this module to remove last week's 168 lists
# !!!IMPORTANT: Don't run until last week's scheduled email blasts have completed.

import interfaces.list, _config

# Returns a list of numerical strings, drawn from list_ids.csv
def _getListIds():
	f = open('%s/list_ids.csv' % _config.DATA_DIR,'r')
	data = f.read()
	f.close()
	return data.split(',')

# Sends a single DELETE request to streamsend to destroy the list with the given id
def _transmitRequest(id):
	response = interfaces.list.destroy(id)
	if response.status != 200:
		print >> sys.err, 'Error deleting list %s' % id
		print >> sys.err, response.status, response.code
		print >> sys.err, response.read()
	else:
		print id+',',

if __name__ == '__main__' and __file__:
	import sys, os
	os.chdir(os.path.dirname(__file__))
	sys.err = open(_config.SYS_ERR_FILE('cleanup'), 'w')
	
	# Get list ids from file
	print 'aquiring list ids...'
	list_ids = _getListIds()
	
	# Delete lists on streamsend
	print 'requesting deletes from streamsend'
	for id in list_ids:
		_transmitRequest(id)
	
	print 'Complete.'
	
# todo: delete following lines, defining list_ids and upload_ids
#list_ids = list(str(i) for i in range(68, 404, 2))
#upload_ids = list(str(i) for i in range(376, 712, 2))
#/todo
