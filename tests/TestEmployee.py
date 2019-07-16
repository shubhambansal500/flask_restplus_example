import unittest
from app import create_app
import json


class TestEmployee(unittest.TestCase):

    def setUp(self):
        self.app = create_app('core.config')
        self.client = self.app.test_client()

        self.data = {"name": "example", "email": "example.com"}
        self.da = {"id": 9, "name": "shubham_updated1", "email": "shubham.bansal@siemens.com"}

    def test_get_data(self):
        response = self.client.get('/employees/')
        self.assertEqual(response.status_code, 200)

    def test_post_and_delete_data(self):
        response = self.client.post('/employees/', data=json.dumps(self.data), content_type='application/json')
        d = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)

        self.dl = {"id": d['data']['id'], "name": "shubham_updated1", "email": "shubham.bansal@siemens.com"}
        response = self.client.delete('/employees/', data=json.dumps(self.dl))
        self.assertEqual(response.status_code, 204)

    def test_patch_data(self):
        response = self.client.patch('/employees/', data=json.dumps(self.da), content_type='application/json')
        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
