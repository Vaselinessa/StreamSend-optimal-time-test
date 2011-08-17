import lxml
from connection import *

# Data should be hash
def create(data={}, aud_id=1):
	resp = request('/audiences/%d/memberships.xml' % int(aud_id), 'POST', data)
	return resp

# Destroys membership of given id for audience of given id	
def destroy(mem_id, aud_id=1):
	resp = request('/audiences/%d/memberships/%d.xml' % (int(aud_id), int(mem_id)), 'DELETE')
	return resp
	
# Returns list of Element[membership] objects for given person.  Data keys: 'page', 'per_page'
def index(per_id, data={'page':1,'per_page':200}, aud_id=1):
	resp = xmlRequest('/audiences/%d/people/%d/memberships.xml' % (int(aud_id), int(per_id)), 'GET', data)
	return tuple(Element(x) for x in resp.iterfind('membership'))
	
def index4list(per_id, list_id, data={'page':1,'per_page':200}, aud_id=1):
	resp = xmlRequest('/audiences/%d/people/%d/lists/%d/memberships.xml' % (int(aud_id), int(per_id), int(list_id)), 'GET', data)
	return tuple(Element(x) for x in resp.iterfind('membership'))

def show(mem_id, aud_id=1):
	resp = xmlRequest('/audiences/%d/memberships/%d.xml' % (int(aud_id), int(mem_id)), 'GET')
	results = tuple(Element(x) for x in resp.iterfind('membership'))
	return results


if __name__ == '__main__':
	# test index()
	#i = index(1)
	# test index()
	p = index(3)
	