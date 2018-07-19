from app import app
import pytest
import unittest
import urllib2

class Test_apis(unittest.TestCase):
    def test_get_one_entry(self):
        tester = app.test_client(self)
        response = tester.get('http://localhost:5000/home/api/v1/entries/1', content_type='application/json')
        mydata = response.data.decode()
        self.assertEqual('{"entry":{"datecreted":"19/7/2018","entrydata":"Milk, Cheese, Pizza, Fruit, Tylenol","id":1}}\n', mydata)

    def test_get_all_entrie(self):
        tester = app.test_client(self)
        response = tester.get('http://localhost:5000/home/api/v1/entries', content_type='application/json')
        entry  = [entry for entry in response.data]
        self.assertEqual('[{"entrylist":[{"datecreted":"19/7/2018","entrydata":"Milk, Cheese, Pizza, Fruit, Tylenol","id":1},{"datecreated":"19/7/2018","entrydata":"Need to find a good Python tutorial on the web","id":2}]}]\n', response.data)

    #def test_get_all_entrie(self):
        #tester = app.test_client(self)
        #response = tester.put('http://localhost:5000/home/api/v1/entries/2', content_type='application/json')
        #entry  = [entry for entry in response.data]
        #self.assertEqual('[{"entrylist":[{"datecreted":"19/7/2018","entrydata":"Milk, Cheese, Pizza, Fruit, Tylenol","id":1},{"datecreated":"19/7/2018","entrydata":"Need to find a good Python tutorial on the web","id":2}]}]\n', response.data)

if __name__ == '__main__':
    unittest.main()


    #Ensure that login page loads correctly
   # def test_get_all_entries(self):
   #     response = tester.get('/login', content_type='html/text')
   #     self.assertTrue('Please login' in response.data)

    #def test_


#[{"entrylist": [{"datecreated": "Wed, 18 Jul 2018 17:52:41 GMT", \
#"entrydata": "new entry data", "id": 1}, {"datecreated": \
#"Wed, 18 Jul 2018 17:52:41 GMT", "entrydata": "Need to \
#find a good Python tutorial on the web", "id": 2}]}]



#data = '{"nw_src": "10.0.0.1/32", "nw_dst": "10.0.0.2/32", "nw_proto": "ICMP", "actions": "ALLOW", "priority": "10"}'
#url = 'http://localhost:5000/home/api/v1/entries/1'
#req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
#f = urllib2.urlopen(req)
#for x in f:
#    print(x)
#f.close()

#curl http://localhost:5000/home/api/v1/entries/2 -X DELETE

#curl -i -H "Content-Type: application/json" -X \
#PUT -d '{"entrydata":"new entry data"}' \
#http://localhost:5000/home/api/v1/entries/1

#curl -i -H "Content-Type: application/json" -X \
#POST -d '{"entrydata":"Read a book"}' \
#http://localhost:5000/home/api/v1/entries

#curl -i http://localhost:5000/home/api/v1/entries

#curl -i http://localhost:5000/home/api/v1/entries/1

#if __name__ == '__main__':
#    unittest.main()