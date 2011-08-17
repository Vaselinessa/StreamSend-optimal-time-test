#
# These methods call for user to supply audience id (always one so far) and person id.

import lxml
from connection import *

def index(data={}, audID=1, **kwargs):
	data = dict(data.items() + kwargs.items())
	url = '/audiences/%d/people.xml' % (int(audID))
	resp = xmlRequest(url, 'GET', data)
	results = tuple(Element(x) for x in resp.iterfind('person'))
	if len(results) == 1:	return results[0]
	else: return results
	
def show(listID, audID=1):
	url = '/audiences/%d/people/%d.xml' % (int(audID), int(listID))
	resp = xmlRequest(url, 'GET')
	return Element(resp)
	
if __name__ == '__main__':
	# test index():
	#a = index()
	#for x in a: print x.id
	# test index() 2:
	a = index(email_address='jonpinney@pinneyinsurance.com')
	if type(a) == tuple: print len(a)
	else: print a.xml()
	# test show():
	#p = show(11)
	#print p.xml()