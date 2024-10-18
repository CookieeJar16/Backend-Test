import unittest
import requests

class RestCalls:
    @staticmethod
    def google_do_something(url):
        try:
            r = requests.get(url, timeout=1)
            r.raise_for_status()
            return r.status_code
        except requests.exceptions.Timeout as errt:
            print(errt)
            raise
        except requests.exceptions.HTTPError as errh:
            print(errh)
            raise
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            raise
        except requests.exceptions.RequestException as err:
            print(err)
            raise

class TestRESTMethods(unittest.TestCase):

    BASE_URL = 'http://localhost:8000'

    def test_valid_google_url(self):
        self.assertEqual(200, RestCalls.google_do_something('http://www.google.com/search'))

    def test_invalid_localhost_url(self):
        self.assertRaises(requests.exceptions.Timeout, RestCalls.google_do_something, 'http://localhost:28989')

    # Testing API Endpoints
    def test_get_categories(self):
        response = requests.get(f'{self.BASE_URL}/categories')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_post_category(self):
        category_data = {"name": "New Category"}
        response = requests.post(f'{self.BASE_URL}/categories', json=category_data)
        self.assertEqual(response.status_code, 201)

        # Test creating the same category again (should fail)
        response = requests.post(f'{self.BASE_URL}/categories', json=category_data)
        self.assertEqual(response.status_code, 409)

    def test_get_items(self):
        response = requests.get(f'{self.BASE_URL}/items')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_item_by_id(self):
        # Assuming there is an item with ID 1
        response = requests.get(f'{self.BASE_URL}/items/1')
        self.assertEqual(response.status_code, 200)

        # Test for a non-existent item
        response = requests.get(f'{self.BASE_URL}/items/999')
        self.assertEqual(response.status_code, 404)

    def test_post_item(self):
        item_data = {
            "category_id": 1,
            "name": "Test Item",
            "description": "This is a test item.",
            "price": 20.99
        }
        response = requests.post(f'{self.BASE_URL}/items', json=item_data)
        self.assertEqual(response.status_code, 201)

        # Test creating the same item again (should fail)
        response = requests.post(f'{self.BASE_URL}/items', json=item_data)
        self.assertEqual(response.status_code, 409)

    def test_put_item(self):
        # Assuming there is an item with ID 1
        updated_item_data = {
            "category_id": 1,
            "name": "Updated Test Item",
            "description": "This is an updated test item.",
            "price": 25.99
        }
        response = requests.put(f'{self.BASE_URL}/items/1', json=updated_item_data)
        self.assertEqual(response.status_code, 200)

        # Test updating a non-existent item
        response = requests.put(f'{self.BASE_URL}/items/999', json=updated_item_data)
        self.assertEqual(response.status_code, 404)

    def test_delete_item(self):
        # Assuming there is an item with ID 1
        response = requests.delete(f'{self.BASE_URL}/items/1')
        self.assertEqual(response.status_code, 204)

        # Test deleting a non-existent item
        response = requests.delete(f'{self.BASE_URL}/items/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
