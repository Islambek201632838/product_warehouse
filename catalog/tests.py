from rest_framework.test import APITestCase
from rest_framework import status

class CatalogTestCase(APITestCase):
    def test_get_catalog(self):
        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ProductDetailTestCase(APITestCase):
    def test_get_product_detail(self):
        product_id = 1  # Replace with a valid product ID for your test database
        response = self.client.get(f'/product/{product_id}/')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

class SearchTestCase(APITestCase):
    def test_search_catalog(self):
        response = self.client.get('/search/?q=test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UpdateStocksTestCase(APITestCase):
    def test_update_stocks(self):
        data = {
            "product_id": 1,  # Replace with a valid product ID for your test database
            "store_id": 1,    # Replace with a valid store ID for your test database
            "quantity": 10,
            "price": 100.0
        }
        response = self.client.post('/catalog/update/stocks/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)