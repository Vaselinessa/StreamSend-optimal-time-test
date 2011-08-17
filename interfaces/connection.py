#
# Just use method 'xmlRequest'

import base64, httplib, urllib, urlparse
from lxml import etree
import _config

def _authKey():
	base = "%s:%s" % (_config.LOGIN_ID, _config.API_KEY)
	header = "Basic %s" % base64.b64encode(base)
	return header


def _request(path=None, method=None, data=None, headers={}):
	# ensure method
	if not method: method = "POST" if data else "GET"
	# ensure headers
	if not headers.has_key('Authorization'): headers['Authorization'] = _authKey()
	# ensure path
	url = urlparse.urlsplit(path)
	path = url.path
	# ensure body (data)
	if data and headers.get('Content-type') in (None, 'text/html'): data = urllib.urlencode(data)
	# request, response
	conn = httplib.HTTPSConnection('app.streamsend.com',443)
	if method == 'GET' and data != None:
		path = path+'?'+data; data = None		
	conn.request(method, path, data, headers)
	return conn.getresponse()
	
# Returns a response or etree
def xmlRequest(path=None, method=None, data=None, headers={}):
	response = _request(path, method, data, headers)
	if response.status == 200:
		return etree.fromstring(response.read())
	else:
		return response

# Wrapper for lxml._Element used in creating requests
class ReqElement(object):
	def addChild(self, tag, text=None):
		child = etree.SubElement(self.root, tag)
		if text != None: child.text = str(text)
		return child
	def diag(self):
		print etree.tostring(self.root, pretty_print=True)
		
# Wrapper for lxml._Element used in interpreting responses
class Element(object):
	def __init__(self, lxml):
		self.lxml = lxml
	def __getattr__(self, key):
		if key == 'lxml': return self.lxml
		if key == 'text': return self.lxml.text
		# handle prefixes, namespace
		key = key.replace('_', '-')
		if ':' in key:
			finds = tuple((Element(x) if x.getchildren() else x.text) for x in self.lxml.findall(key, self.lxml.nsmap))
		elif self.lxml.nsmap.has_key(None):
			key = "{%s}key" % self.lxml.nsmap[None]
			finds = tuple((Element(x) if x.getchildren() else x.text) for x in self.lxml.findall(key))
		else:
			finds = tuple((Element(x) if x.getchildren() else x.text) for x in self.lxml.findall(key))
		if len(finds) == 0:
			raise Exception(key, "attribute not found in Element instance.")
		elif len(finds) == 1:
			return finds[0]
		else:
			return finds
	def evaluate(self):
		if self.lxml.getchildren(): return self
		else: return self.text
	def xml(self, pretty_print=True):
		return etree.tostring(self.lxml, pretty_print=pretty_print)
		
if __name__ == '__main__':
	resp = xmlRequest('/audiences.xml', 'GET')
	print etree.resp.tostring()