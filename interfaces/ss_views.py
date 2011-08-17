#
import sys
from lxml import etree
import connection, utils

# Returns http response (should hold <views><view />...<views>)
def index(blastID, data={'per_page':10000, 'page':1}, **kwargs):
	data = dict(data.items() + kwargs.items())
	url = '/blasts/%d/views.xml' % int(blastID)
	resp = connection._request(url , 'GET', data)
	return resp
	
class View(utils.Response):
	def __init__(self, etreeElement):
		self.element = etreeElement
		#self._init_field('blast_id','blast-id')
		self._init_field('person_id','.//person-id')
		self._init_field('id','.//id')
	