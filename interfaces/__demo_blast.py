from blast import *

def testCreate():
	global resp
	import datetime
	fpath = 'C:\\Documents and Settings\\markhama\\My Documents\\coding\\stream_send\\data\\blast.xml'
	dt = datetime.datetime.now() + datetime.timedelta(hours = 5)
	dts = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
	b = Blast(fpath, dts)
	print etree.tostring(b.xml)
	resp = b.create()
	print resp.status, resp.reason
	print utils.getId(resp)

def testIndex():
	global resp
	resp = index(page=1, per_page=10)
	print resp.status, resp.reason
	print resp.read()
	
def testShow(id):
	global resp
	resp = show(id)
	print resp.status, resp.reason
	print resp.read()
	
def testTest(recipients):
	global resp
	import datetime
	fpath = 'C:\\Documents and Settings\\markhama\\My Documents\\coding\\stream_send\\data\\blast.xml'
	dt = datetime.datetime.utcnow() + datetime.timedelta(hours = 5)
	dts = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
	b = Blast(fpath, dts)
	resp = b.test(recipients)
	print resp.status, resp.reason
	
# test module
if __name__ == '__main__':
	#testCreate()
	#testIndex()
	#testShow(14199629)
	testTest('manderson@pinneyinsurance.com')