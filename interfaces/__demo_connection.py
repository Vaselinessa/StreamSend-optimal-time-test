import connection
from connection import *

def test_req():
	return connection._request('/audiences.xml', 'GET')
	
if __name__ == '__main__':
	resp = test_req()