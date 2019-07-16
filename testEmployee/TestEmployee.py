import unittest
import json
from app import app


class TestEmployee(unittest.TestCase):

    appTest =app

    def setUp(self):
        #self.app = create_app('config')
        self.client = self.appTest.test_client()

        self.data = {"name": "example", "email": "example.com"}
        self.da = {"id": 9, "name": "shubham_updated1", "email": "shubham.bansal@siemens.com"}

    def test_get_data(self):
        response = self.client.get('/employee/')
        self.assertEqual(response.status_code, 200)

    def test_post_and_delete_data(self):
        response = self.client.post('/employee/', data=json.dumps(self.data), content_type='application/json')
        d = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)

        self.dl = {"id": d['data']['id'], "name": "shubham_updated1", "email": "shubham.bansal@siemens.com"}
        response = self.client.delete('/employee/', data=json.dumps(self.dl))
        self.assertEqual(response.status_code, 204)

    def test_patch_data(self):
        response = self.client.patch('/employee/', data=json.dumps(self.da), content_type='application/json')
        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
