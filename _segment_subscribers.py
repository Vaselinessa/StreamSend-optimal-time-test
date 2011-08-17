#
# Called by module 'brain'.
# Gets subscribes from subscribers_src_file ('My Subscribers.txt') and randomly sorts them into 
# 168 lists of equal length, contained in files in directory '168-user-lists'

import os, random, re

fileIndices = []
	
# run
def run(subscribers_src_file, subscribers_dst_dir, ignore_first_line):
	os.chdir(os.path.dirname(__file__))
	if os.path.exists(subscribers_src_file):
		global files
		# get input and output files
		subscribers = open(subscribers_src_file, 'r')
		files = _getArrayOfFiles(subscribers_dst_dir)
		if ignore_first_line: subscribers.readline()
		# loop through lines of input file
		for line in subscribers:
			_handleSubscriber(line)
		for file in files:
			file.close()
		subscribers.close()

# Returns a random file index 0-167.
# Ensures that each index is issued an equal number of times.
# When fileIndices is empty, fills it with range(0,167)
def _getRand():
	global fileIndices
	if len(fileIndices) == 0:
		fileIndices = random.sample(xrange(168), 168)
	return fileIndices.pop()
		
# Takes a line of text (from subscribers_src_file), extracts email, writes line to destination file
def _handleSubscriber(line):
	idx = _getRand()
	match = re.match('[^\t]+', line)
	email = match.group()
	if len(email) > 1:
		files[idx].write(email)
		files[idx].write('\n')

# Returns array of 168 open file objects
def _getArrayOfFiles(directory):
	files = []
	for i in range(0, 168):
		fpath = "%s/%d.txt" % (directory, i)
		files.append(open(fpath, 'w'))
	return files