"""this is an testing file in which unit-testing is performed """
import unittest
from unittest.mock import patch
import json
from app import app


class FakeResponse:
    @classmethod
    def response(cls):
        return {}


class ApiTest(unittest.TestCase):

    def test_get_with_category(self):
        with patch('resources.inventory.InventoryModel.find_by_category',
                   return_value=FakeResponse.response()) as mocked:
            tester = app.test_client()
            response = tester.get('/inventory?category=study-material')
            self.assertEqual(response.status_code, 404)

    def test_get_with_name(self):
        with patch('resources.inventory.InventoryModel.find_by_name', return_value=FakeResponse.response()) as mocked:
            tester = app.test_client()
            response = tester.get('/inventory?inventory_name=pencil')
            self.assertEqual(response.status_code, 404)

    def test_get_with_name_category(self):
        with patch('resources.inventory.InventoryModel.find_by_name_and_category',
                   return_value=FakeResponse.response()) as mocked:
            tester = app.test_client()
            response = tester.get('/inventory?inventory_name=pencil&category=study-material')
            self.assertEqual(response.status_code, 404)

    def test_put(self):
        with patch('resources.inventory.InventoryModel.find_by_id', return_value=FakeResponse.response()) as mocked:
            tester = app.test_client()
            data = json.dumps({'inventory_id': 1, 'quantity': 25})
            response = tester.put('/inventory/update', content_type='application/json', data=data)
            self.assertEqual(response.status_code, 404)

    def test_delete(self):
        with patch('resources.inventory.InventoryModel.find_by_name', return_value=FakeResponse.response()) as mocked:
            tester = app.test_client()
            data = json.dumps({'inventory_name': 'pencil'})
            response = tester.delete('/inventory/delete', content_type='application/json', data=data)
            self.assertEqual(response.status_code, 404)

    def test_post(self):
        with patch('resources.inventory.InventoryModel.insert', return_value=FakeResponse.response()) as mocked:
            tester = app.test_client()
            data = json.dumps({"inventory_name": "pencil", "inventory_category": "study", "quantity": 200,
                               "manufacturing_date": "18-12-2019 12:00:+05:30"})
            response = tester.post('/inventory', content_type='application/json', data=data)
            self.assertEqual(response.status_code,
                             201)  # here we matching 503 beacause we are not posting image.
