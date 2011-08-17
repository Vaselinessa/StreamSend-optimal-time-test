#
# These methods call for user to supply audience id (always one so far) and list id.

from lxml import etree
import connection
from connection import *
	
# Returns the response (after printing code and reason)
def destroy(listID, audID=1):
	url = '/audiences/%d/lists/%d.xml' % (int(audID), int(listID))
	#print url
	resp = connection._request(url, 'DELETE')
	#print resp.status, resp.reason
	return resp
	
# Returns tuple of connection.Element objects
def index(audID=1):
	url = '/audiences/%d/lists.xml' % (int(audID))
	resp = xmlRequest(url, 'GET')
	return tuple(Element(x) for x in resp.iterfind('list'))

# Returns tuple of connection.Element objects	
def index4Person(perID, audID=1):
	url = '/audiences/%d/people/%d/lists.xml' % (int(audID), int(perID))
	resp = xmlRequest(url, 'GET')
	return tuple(Element(x) for x in resp.iterfind('list'))
	
# Returns instance of connection.Element
def show(listID, audID=1):
	url = '/audiences/%d/lists/%d.xml' % (int(audID), int(listID))
	resp = xmlRequest(url, 'GET')
	return Element(resp)
	
class List(connection.ReqElement):
	def __init__(self, name, description=None):
		self.root 	= etree.Element("list")
		self.setName(name)
		if description: self.setDesc(description)
	def setName(self, value):
		self.setName = None
		return self.addChild("name", value)
	def setDesc(self, value):
		self.setDesc = None
		return self.addChild("description", value)
	def create(self, audID=1):
		url = '/audiences/%d/lists.xml' % int(audID)
		data = etree.tostring(self.root, pretty_print=False)
		headers = {'Content-type':'application/xml'}
		resp = connection._request(url, 'POST', data, headers)
		'''print resp.status
		for header in resp.getheaders():
			if header[0] == 'location': print header[1]; break'''
		return resp