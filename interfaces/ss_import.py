#
# api: http://app.streamsend.com/docs/api/classes/ImportsController.html

from lxml import etree
import connection

def show(importId, audId=1):
	url = '/audiences/%d/imports/%d.xml' % (audId, importId)
	resp = connection._request(url, 'GET')
	if resp.status < 300 and resp.status >= 200:
		return connection.Element(etree.fromstring(resp.read()))

class Import(connection.ReqElement):
	def __init__(self, uploadId=None, separator='Tab', *lists):
		self.root = root	 = etree.Element("import")
		self.reactivate		= self.addChild("reactivate")
		self.lists				= self.addChild("lists")
		self.ignoreFirst	=	self.addChild("ignore_first_row", "false")
		self.id 					= self.addChild("upload_id", uploadId)
		self.separator		= self.addChild("separator", separator)
		self.columns 			= self.addChild("columns")
		self.setLists(*lists)
	def setLists(self, *ids):
		self.lists.text = ','.join(str(id) for id in ids)
	def showCols(self):
		print etree.tostring(self.columns, pretty_print=True)
	def addCol(self, text):
		col = etree.SubElement(self.columns, "column")
		col.text = text
		return col
	# Send this data to StreamSend, return response
	def create(self, audID=1):
		url = '/audiences/%d/imports.xml' % audID
		headers = {'Content-type':'application/xml'}
		data = etree.tostring(self.root, pretty_print=False)
		resp = connection._request(url, 'POST', data, headers)
		'''print resp.status
		for header in resp.getheaders():
			if header[0] == 'location': print header[1]; break'''
		return resp
	
