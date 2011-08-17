#
# Called by setup.py
# run() executes imports for each list_id and upload_id supplied

import sys
from interfaces.ss_import import Import
import interfaces.utils as utils

def run(list_ids, upload_ids):
	import_ids = []
	for i in range(min(len(list_ids), len(upload_ids))):
		# create Import instance
		imp = Import(upload_ids[i])
		imp.addCol('email_address')
		imp.setLists(list_ids[i])
		# execute http transfer
		try:
			resp = imp.create()
			id = utils.getId(resp)
			import_ids.append(id)
			print id, 
		except utils.HttpException as err:
			print >> sys.err, 'Exception at _streamsend_imports.py#run() - line 18-21'
			print >> sys.err, '\t', err
	print
	return import_ids
		