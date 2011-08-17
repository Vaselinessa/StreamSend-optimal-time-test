from list import *

def testCreate():
	global resp
	#xml = List('Markham temp list', 'Wouldn\'t it be lovely?')
	xml = List('Markham temp list')
	print etree.tostring(xml.root)
	xml.diag()
	xml.create()
	
def testShow(id):
	global l
	l = show(id)
	print l.xml()
	
def testIndex():
	global a
	a = tuple(index())
	for x in a: print x.id
	print a[0].xml()
	
def testDestroy(id):
	global resp
	resp = destroy(id)
	print resp.read()
	
if __name__ == '__main__':
	#testCreate()
	#testIndex()
	testShow(11)
	#testDestroy(66)