#
# Running this file as main module will:
# 1. get email addresses from a file defined as _config.SUBSCRIBERS_FILE
# 2. divide list of email addresses into 168 groups of equal (+-1) size
# 3. write each group to a file in _config.DIR_OF_USER_LISTS
# 4. create 168 lists at streamsend, named 'blast 0' through 'blast 167'; (write ids to list_ids.csv)
# 5. upload each of the 168 files of email addresses created in step 2-3 to streamsend; (write ids to upload_ids.csv)
# 6. import each upload to a corresponding streamsend list; (write ids to import_ids.csv)
# Result: 168 lists, populated with a random sample of users from the original _config.SUBSCRIBERS_FILE file

import sys, os
import _config
import _segment_subscribers
import _streamsend_lists
import _streamsend_uploads
import _streamsend_imports

def logIds(name, ids):
	fpath = '%s/%s.csv' % (_config.DATA_DIR, name)
	f = open(fpath, 'w')
	f.write(','.join(ids))
	f.close()

if __name__ == '__main__' and __file__:
	os.chdir(os.path.dirname(__file__))
	sys.err = open(_config.SYS_ERR_FILE('setup'), 'w')
	
	# create 168 list files
	print 'creating, populating files in dir "%s"...' % _config.DIR_OF_USER_LISTS
	_segment_subscribers.run(_config.SUBSCRIBERS_FILE, _config.DIR_OF_USER_LISTS, _config.IGNORE_FIRST_LINE_OF_SUBSCRIBERS)
	# create 168 lists on StreamSend
	print 'creating lists on streamsend...'
	list_ids = _streamsend_lists.run()
	logIds('list_ids', list_ids)
	# execute 168 uploads
	print 'uploading %s files to streamsend...' % _config.DIR_OF_USER_LISTS
	upload_ids = _streamsend_uploads.run()
	logIds('upload_ids', upload_ids)
	# execute 168 imports
	print 'executing imports on streamsend...'
	import_ids = _streamsend_imports.run(list_ids, upload_ids)
	logIds('import_ids', import_ids)
	
	sys.err.close()
	print 'Completed.'