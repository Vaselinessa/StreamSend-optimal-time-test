import lxml
from connection import *

# Returns list of Element[audience] objects
def index():
	resp = xmlRequest('/audiences.xml', 'GET')
	return (Element(x) for x in resp.iterfind('audience'))
	
# Returns an instance of Element[audience]
def show(id=1):
	resp = xmlRequest('/audiences/%d.xml' % int(id), 'GET')
	return Element(resp)

# ***untested
def update(id=1, data={}):
	resp = request('/audiences/%d' % int(id), 'PUT', data)
	return resp

if __name__ == '__main__':
	a = show()
	print a.xml()
	print a.name
	print a.id
	