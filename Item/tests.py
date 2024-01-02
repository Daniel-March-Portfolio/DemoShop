from django.conf import settings
from django.test import TestCase
from requests import Response

from Category.models import Category
from Item.models import Item


class SimpleTest(TestCase):
    def setUp(self) -> None:
        self.category_1 = Category.objects.create(title="Test 1")
        self.category_2 = Category.objects.create(title="Test 2")

    def test_details(self):
        item = Item.objects.create(
            title=f"Test item",
            description=f"Test item description",
            price=100,
            category=self.category_1,
        )

        response: Response = self.client.get(f"/api/items/{item.uuid}/")
        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        self.assertEqual(
            response_data,
            {
                "uuid": str(item.uuid),
                "title": item.title,
                "description": item.description,
                "price": item.price,
                "category": str(item.category.uuid)
            }
        )

    def test_list(self):
        for i in range(settings.REST_FRAMEWORK["PAGE_SIZE"] + 1):
            Item.objects.create(
                title=f"Test item {i}",
                description=f"Test item {i} description",
                price=100,
                category=self.category_1,
            )

        response: Response = self.client.get(f"/api/items/")
        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        self.assertIn("results", response_data, response_data)
        self.assertIn("count", response_data, response_data)

        self.assertEqual(response_data["count"], settings.REST_FRAMEWORK["PAGE_SIZE"] + 1, response_data)
        self.assertNotEqual(response_data["next"], None, response_data)
        self.assertEqual(response_data["previous"], None, response_data)
        self.assertEqual(len(response_data["results"]), settings.REST_FRAMEWORK["PAGE_SIZE"], response_data)

        response: Response = self.client.get(response_data["next"])
        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        self.assertIn("results", response_data, response_data)
        self.assertIn("count", response_data, response_data)
        self.assertEqual(response_data["count"], settings.REST_FRAMEWORK["PAGE_SIZE"] + 1, response_data)
        self.assertNotEqual(response_data["previous"], None, response_data)
        self.assertEqual(response_data["next"], None, response_data)
        self.assertEqual(len(response_data["results"]), 1, response_data)

    def test_filter(self):
        n_category_1_items = 5
        n_category_2_items = 3
        self.assertGreaterEqual(settings.REST_FRAMEWORK["PAGE_SIZE"], n_category_1_items + n_category_2_items)
        for i in range(n_category_1_items):
            Item.objects.create(
                title=f"Test item {i} in category_1",
                description=f"Test item {i} description in self.category_1",
                price=100,
                category=self.category_1,
            )
        for i in range(n_category_2_items):
            Item.objects.create(
                title=f"Test item {i} in category_2",
                description=f"Test item {i} description in category_2",
                price=100,
                category=self.category_2,
            )

        response: Response = self.client.get(f"/api/items/?category={self.category_1.uuid}")
        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        self.assertIn("results", response_data, response_data)
        self.assertIn("count", response_data, response_data)
        self.assertEqual(response_data["count"], n_category_1_items, response_data)

        response: Response = self.client.get(f"/api/items/?category={self.category_2.uuid}")
        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        self.assertIn("results", response_data, response_data)
        self.assertIn("count", response_data, response_data)
        self.assertEqual(response_data["count"], n_category_2_items, response_data)
