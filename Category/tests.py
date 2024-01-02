from django.conf import settings
from django.test import TestCase
from requests import Response

from Category.models import Category


class SimpleTest(TestCase):
    def test_details(self):
        category = Category.objects.create(title="Test")

        response: Response = self.client.get(f"/api/categories/{category.uuid}/")
        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        self.assertEqual(
            response_data,
            {
                "uuid": str(category.uuid),
                "title": category.title,
            }
        )

    def test_list(self):
        for i in range(settings.REST_FRAMEWORK["PAGE_SIZE"] + 1):
            Category.objects.create(title=f"Test {i}")

        response: Response = self.client.get(f"/api/categories/")
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
