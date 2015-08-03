import os
import task2
import unittest
import tempfile
import json

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, task2.app.config['DATABASE'] = tempfile.mkstemp()
        task2.app.config['TESTING'] = True
        self.app = task2.app.test_client()
        task2.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(task2.app.config['DATABASE'])
        
    def test_api(self):
      # verify list is empty
      print "GET request to /vpn/"
      response = self.app.get('/vpn/?mylat=0&mylong=0')
      print response.data
      assert json.loads(response.data)['VPNs'] == []
      
      # verify VPN can be added
      print "POST request to /vpn/test1"
      response = self.app.post('/vpn/test1', data=dict(lat=1.0, long=2))
      print response.status_code
      assert response.status_code == 201
      
      # verify another VPN can be added
      print "POST request to /vpn/test2"
      response = self.app.post('/vpn/test2', data=dict(lat=-10, long=10))
      print response.status_code
      assert response.status_code == 201
      
      # verify VPNs are listed in correct order
      print "GET request to /vpn/"
      response = self.app.get('/vpn/?mylat=0&mylong=0')
      print response.data
      assert json.loads(response.data)['VPNs'] == [{ 'name': 'test1', 'latitude': 1, 'longitude': 2 }, { 'name': 'test2', 'latitude': -10, 'longitude': 10 }]
      
      # verify VPNs are listed in correct order from a different point
      print "GET request to /vpn/"
      response = self.app.get('/vpn/?mylat=-5&mylong=8')
      print response.data
      assert json.loads(response.data)['VPNs'] == [{ 'name': 'test2', 'latitude': -10, 'longitude': 10 }, { 'name': 'test1', 'latitude': 1, 'longitude': 2 }]

      # verify a VPN can be deleted
      print "DELETE request to /vpn/test1"
      response = self.app.delete('/vpn/test1')
      print response.status_code
      assert response.status_code == 204
      
      # verify remaining VPN is unaffected
      print "GET request to /vpn/"
      response = self.app.get('/vpn/?mylat=0&mylong=0')
      print response.data
      assert json.loads(response.data)['VPNs'] == [{ 'name': 'test2', 'latitude': -10, 'longitude': 10 }]
      
if __name__ == '__main__':
    unittest.main()