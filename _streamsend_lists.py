#
# call run().
# Creates 168 lists on Streamsend.

import os
from interfaces.list import List

# Creates 168 lists on Streamsend. Returns their id numbers.
def run():
	ids = []
	for i in range(168):
		name = "blast %d" % i
		resp = List(name).create()
		id = getId(resp)
		ids.append(id)
		print ("{%d:%s} " % (i, id)),
	print
	return ids
		
# Gets list id from httpresponse headers
def getId(httpresponse):
	if httpresponse.status < 300 and httpresponse.status >= 200:
		for header in httpresponse.getheaders():
			if header[0] == 'location': location = header[1]; break
		id = os.path.basename(location)
		return id

if __name__ == '__main__':
	ls = List('temp for Markham')
	from lxml import etree
	print etree.tostring(ls.root, pretty_print=True)