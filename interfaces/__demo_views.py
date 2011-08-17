from ss_views import *

def test_index():
	global results
	results = index(14205017)
	print len(results)
	
if __name__ == '__main__':
	test_index()