# 
# Used for diag.  Run through lists in _config.DIR_OF_USER_LISTS, and ensure that no two lines are identical.

import glob, os
import _config

os.chdir(os.path.dirname(__file__))

emails 	= []
files		= glob.iglob('%s/*.txt' % _config.DIR_OF_USER_LISTS)

for file in files:
	print file, '...'
	f = open(file, 'r')
	for line in f:
		if line in emails:
			print 'ERROR - DUPLICATE EMAIL: %s' % line.strip()
			print '... in file %s' % file
			print '... matches list index %d' % len(emails)
			break
		else:
			emails.append(line)
	f.close()
print 'Completed.'