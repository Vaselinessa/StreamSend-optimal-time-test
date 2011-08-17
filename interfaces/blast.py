#

import urllib, datetime, re
from lxml import etree
import connection, utils

# Destroys a scheduled blast on streamsend
def destroy(blast_id, aud_id=1):
	url = '/audiences/%s/blasts/%s.xml' % (str(aud_id), str(blast_id))
	resp = connection._request(url, 'DELETE')
	return resp

def index(data={}, aud_id=1, **kwargs):
	data = dict(data.items() + kwargs.items())
	url = '/audiences/%s/blasts.xml' % str(aud_id)
	if data: url += '?%s' % urllib.urlencode(data)
	resp = connection._request(url, 'GET')
	return resp
	
# Returns an http response for given blast
def show(blast_id, aud_id=1):
	url = '/audiences/%s/blasts/%s.xml' % (str(aud_id), str(blast_id))
	resp = connection._request(url, 'GET')
	return resp
	
class Response(utils.Response):
	def __init__(self, etreeElement):
		self.element = etreeElement
		self._init_field('scheduled_for','scheduled-for')
		self._init_field('id','id')
	def datetime(self):
		ts = self.scheduled_for
		return datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ')
	@classmethod
	def forId(cls, id):
		response = show(id)
		return cls.fromHttp(response)

class Blast(connection.ReqElement):
	# Reads file at fpath to get subject and email_id for email
	def __init__(self, fpath, timestamp=None, list_ids=()):
		self.xml = etree.parse(fpath)
		if timestamp:	self.setTimestamp(timestamp)
		if list_ids:	self.setLists(list_ids)
	def setTimestamp(self, timestamp):
		if isinstance(timestamp, datetime.datetime):
			timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
		self.xml.xpath('/blast/scheduled-for')[0].text = timestamp
	# Sets recipient lists. Expects iterable
	def setLists(self, list_ids):
		str_ids = ','.join(list_ids)
		self.xml.xpath('/blast/to/include-lists')[0].text = str_ids
	# todo: timing of scheduling doesn't apepar to be working
	def create(self, audId=1):
		url = '/audiences/%s/blasts.xml' % str(audId)
		headers = {'Content-type':'application/xml'}
		##data = etree.tostring(self.xml, with_comments=False)
		data = self.tostring()
		resp = connection._request(url, 'POST', data, headers)
		return resp
	def test(self, recipients, audId=1):
		url = '/audiences/%s/blasts/test.xml' % str(audId)
		headers = {'Content-type':'application/xml'}
		# handle recipients
		if type(recipients) != str: recipients = ','.join(recipients)
		toNode = self.xml.xpath('/blast/to')[0]
		etree.strip_elements(toNode, 'audience-id', 'include-lists')
		toNode.text = recipients
		# send request
		##data = etree.tostring(self.xml, with_comments=False)
		data = self.tostring()
		resp = connection._request(url, 'POST', data, headers)
		return resp
	def tostring(self, pretty_print=False, nix_comments=True):
		text = etree.tostring(self.xml.getroot(), pretty_print=pretty_print)
		if nix_comments: text = re.sub(r'(\s*)<!--(.*?)-->',r'',text)
		return text

	