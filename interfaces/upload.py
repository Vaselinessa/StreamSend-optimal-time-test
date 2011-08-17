#
# The only method to call from this module is 'create'
# See the api: http://app.streamsend.com/docs/api/classes/UploadsController.html

import httplib, urllib, os, mimetypes
import connection

# Used for encoding any number of datafields and files for http transfer.
# 'fields' is iterable of (key, value)
# 'files' is iterable of (key, filename, value)
# Returns (content-type, encoded data) ready for http transfer
def __encode_multipart(fields, files):
	BOUNDARY  = '@#$7890BoUnDARY_$'
	CRLF 			= '\r\n'
	L 				= []
	for (key, value) in fields:
		L.append('--' + BOUNDARY)
		L.append('Content-Disposition: form-data; name="%s"' % key)
		L.append('')
		L.append(value)
	for (key, filename, value) in files:
		L.append('--' + BOUNDARY)
		L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
		L.append('Content-Type: %s' % mimetypes.guess_type(filename)[0] or 'application/octet-stream')
		L.append('')
		L.append(value)
	L.append('--' + BOUNDARY + '--')
	L.append('')
	body = CRLF.join(L)
	content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
	return content_type, body

# Calls _encode_multipart using only a single file as data to be transferred
# Returns (content-type, encoded data) ready for http transfer
def _format_data(filename):
	f = open(filename)
	data = f.read()
	f.close()
	return __encode_multipart([],[('data', filename, data)])
	
# Returns id of uploadif successful (201).  Raises Exception otherwise
def create(fpath):
	content_type, data = _format_data(fpath)
	headers = {
		'Content-Type'		:content_type,
		'Authorization'		:connection._authKey(),
		'Accept'					:'application/xml'
	}
	conn = httplib.HTTPSConnection('app.streamsend.com',443)
	conn.request('POST', '/uploads', data, headers)
	resp = conn.getresponse()
	return resp