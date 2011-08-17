from upload import *

def _test():
	path = '/uploads'
	fpath = 'c:/documents and settings/markhama/my documents/coding/stream_send/data.txt'
	method = 'POST'
	f = open(fpath)
	value = f.read()
	f.close()
	content_type, data = encode_multipart([], [('data',fpath,value)])
	headers = {}
	headers['Content-Type'] = content_type
	headers['Authorization'] = connection._authKey()
	headers['Accept'] = 'application/xml'
			
	conn = httplib.HTTPSConnection('app.streamsend.com',443)
	conn.request(method, path, data, headers)
	resp = conn.getresponse()
	print resp.status
	print resp.getheaders()
	
if __name__ == '__main__':
	print create('c:/documents and settings/markhama/my documents/coding/stream_send/data.txt')