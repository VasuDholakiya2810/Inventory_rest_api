'''this is an testing file in which unit-testing is performed '''
import unittest
from unittest.mock import patch
import json
from run import app

class ApiTest(unittest.TestCase):

    def test_get_with_category(self):
        def fake():
            return {}

        with patch('resources.inventory.InventoryModel.find_by_category', return_value=fake()) as mocked:
            tester = app.test_client()
            response = tester.get('/inventory?category=study-material')
            self.assertEqual(response.status_code, 404)

    def test_get_with_name(self):
        def fake():
            return {}

        with patch('resources.inventory.InventoryModel.find_by_name', return_value=fake()) as mocked:
            tester = app.test_client()
            response = tester.get('/inventory?inventory_name=pencil')
            self.assertEqual(response.status_code, 404)

    def test_get_with_name_category(self):
        def fake():
            return {}

        with patch('resources.inventory.InventoryModel.find_by_name_and_category', return_value=fake()) as mocked:
            tester = app.test_client()
            response = tester.get('/inventory?inventory_name=pencil&category=study-material')
            self.assertEqual(response.status_code, 404)

    def test_put(self):
        def fake():
            return {}

        with patch('resources.inventory.InventoryModel.find_by_id', return_value=fake()) as mocked:
            tester = app.test_client()
            data = json.dumps({'id': 1, 'quantity': 25})
            response = tester.put('/inventory',content_type='multipart/form-data',data={'data':data})
            self.assertEqual(response.status_code, 404)


    def test_delete(self):
        def fake():
            return {}

        with patch('resources.inventory.InventoryModel.find_by_name', return_value=fake()) as mocked:
            tester = app.test_client()
            data = json.dumps({'inventory_name':'pencil'})
            response = tester.delete('/inventory',content_type='multipart/form-data',data={'data':data})
            self.assertEqual(response.status_code, 404)

    def test_post(self):
        def fake():
            return {}

        with patch('resources.inventory.InventoryModel.find_by_name', return_value=fake()) as mocked:
            tester = app.test_client()
            data=json.dumps({"inventory_name":"pencil","inventory_category": "study-material","quantity": 200,"manufacturing_date": "18-12-2019 9:15 GMT"})
            response = tester.post('/inventory',content_type='multipart/form-data',data={'data':data})
            self.assertEqual(response.status_code, 503) #here we matching 503 beacause we are not entering posting image.
