#

import os
from lxml import etree

class Response(object):
	# constructor should set self.element (lxml.etree.Element)
	def _init_field(self, attrname, xpath):
		node = self.element.xpath(xpath)[0]
		value = node.text if node != None else None
		self.__setattr__(attrname, value)
	def tostring(self):
		return etree.tostring(self.element)
	@classmethod
	def fromHttp(cls, httpresponse):
		data = httpresponse.read()
		tree = etree.fromstring(data)
		return cls(tree)

class HttpException(Exception):
	def __init__(self, httpResponse):
		Exception.__init__(self, "Exception handling http response.")
		self.response = httpResponse
		httpResponse.data = self.data = httpResponse.read()
	def __repr__(self):
		print self.resp.status,
		print self.resp.reason
		print self.data
		return "%s\n:%d %s\n%s" % (self.message, self.resp.status, self.resp.reason, self.data)

# Extracts id (os.path.basename) from 'location' header in http response
def getId(httpresp):
	if httpresp.status == 201:
		hh = httpresp.getheaders()
		for x in hh:
			if x[0] == 'location':
				return os.path.basename(x[1])
	else:
		raise HttpException(httpresp)