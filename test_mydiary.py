from app import app
import pytest
import unittest

 
class Test_apis(unittest.TestCase):
    def test_get_one_entry_data(self):
        tester = app.test_client(self)
        response = tester.get('http://localhost:5000/home/api/v1/entries/2', content_type='application/json')
        self.assertIn('this is my second entry', response.data)
       
    def test_get_one_entry_status_code(self):
        tester = app.test_client(self)
        response = tester.get('http://localhost:5000/home/api/v1/entries/2', content_type='application/json')
        self.assertEqual(response.status_code, 200)
 
    def test_get_all_entries_data(self):
        tester = app.test_client(self)
        response = tester.get('http://localhost:5000/home/api/v1/entries', content_type='application/json')
        self.assertIn('this is my first entry', response.data)
        self.assertIn('this is my second entry', response.data)
 
    def test_get_all_entries_status_code(self):
        tester = app.test_client(self)
        response = tester.get('http://localhost:5000/home/api/v1/entries', content_type='application/json')
        self.assertEqual(response.status_code, 200)
 
    def test_add_new_entry_status_code(self):
        tester = app.test_client(self)
        response = tester.post('http://localhost:5000/home/api/v1/entries', data='{"entrydata":"New entry data for post test"}', content_type='application/json')
        self.assertEqual(response.status_code, 200)
 
    def test_add_new_entry_data(self):
        tester = app.test_client(self)
        response1 = tester.post('http://localhost:5000/home/api/v1/entries', data='{"entrydata":"New entry data for post test"}', content_type='application/json')
        response2 = tester.get('http://localhost:5000/home/api/v1/entries', content_type='application/json')
        self.assertIn('New entry data for post test', response2.data)
 
    def test_update_entry_status_code(self):
        tester = app.test_client(self)
        response = tester.put('http://localhost:5000/home/api/v1/entries/2', data='{"entrydata":"New entry data for put test"}', content_type='application/json')
        self.assertEqual(response.status_code, 200)
 
    def test_update_entry_data(self):
        tester = app.test_client(self)
        response = tester.post('http://localhost:5000/home/api/v1/entries', data='{"entrydata":"test data"}', content_type='application/json')
        response = tester.put('http://localhost:5000/home/api/v1/entries/1', data='{"entrydata":"New entry data for put test"}', content_type='application/json')
        self.assertIn('New entry data for put test', response.data)
 
    def test_delete_entry_status_code(self):
        tester = app.test_client(self)
        response = tester.post('http://localhost:5000/home/api/v1/entries', data='{"entrydata":"Delete test"}', content_type='application/json')
        response1 = tester.get('http://localhost:5000/home/api/v1/entries', content_type='application/json')
 
        self.assertIn('Delete test', response1.data)
 
        for entry in response1.json[0]["entrylist"]:
            if "Delete test" in entry["entrydata"]:
                response2 = tester.delete('http://localhost:5000/home/api/v1/entries/'+str(entry["id"]), content_type='application/json')
                response3 = tester.get('http://localhost:5000/home/api/v1/entries', content_type='application/json')
                self.assertEqual(response.status_code, 200)
           
    def test_delete_entry_data(self):
        tester = app.test_client(self)
        response = tester.post('http://localhost:5000/home/api/v1/entries', data='{"entrydata":"Delete test"}', content_type='application/json')
        response1 = tester.get('http://localhost:5000/home/api/v1/entries', content_type='application/json')
 
        self.assertIn('Delete test', response1.data)
 
        for entry in response1.json[0]["entrylist"]:
            if "Delete test" in entry["entrydata"]:
                response2 = tester.delete('http://localhost:5000/home/api/v1/entries/'+str(entry["id"]), content_type='application/json')
                response3 = tester.get('http://localhost:5000/home/api/v1/entries', content_type='application/json')
                self.assertNotIn('Delete test', response3.data)
 
if __name__ == '__main__':
    unittest.main()
 
#curl http://localhost:5000/home/api/v1/entries/2 -X DELETE
#curl -i -H "Content-Type: application/json" -X PUT -d '{"entrydata":"new entry data"}' http://localhost:5000/home/api/v1/entries/1
#curl -i -H "Content-Type: application/json" -X POST -d '{"entrydata":"Read a book"}' http://localhost:5000/home/api/v1/entries
#curl -i http://localhost:5000/home/api/v1/entries
#curl -i http://localhost:5000/home/api/v1/entries/1