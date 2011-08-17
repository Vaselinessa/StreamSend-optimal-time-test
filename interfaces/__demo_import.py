imp = __import__('ss_import')

def _test():
	i = imp.Import()
	i.setLists(1,2,5)
	i.addCol('email_address')
	i.diag()
	
# actually commits changes to streamsend
def _testCreate():
	global resp
	#userID = 3
	uploadID = 22
	i = imp.Import(uploadID)
	i.addCol('email_address')
	i.setLists(66)
	i.diag()
	resp = i.create()
	
def _testShow():
	global resp
	resp = imp.show(274)
	print resp.status
	print resp.xml()
	
if __name__ == '__main__':
	#_test()
	_testCreate()
	#_testShow()