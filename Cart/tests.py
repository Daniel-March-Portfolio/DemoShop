from django.conf import settings
from django.contrib.sessions.models import Session
from django.test import TestCase
from django.utils import timezone
from requests import Response

from Cart.models import Cart
from Category.models import Category
from Item.models import Item


class SimpleTest(TestCase):
    def setUp(self) -> None:
        self.setup_session()
        self.category = Category.objects.create(title="Test")
        self.item_1 = Item.objects.create(
            title=f"Test item 1",
            description=f"Test item 1 description",
            price=100,
            category=self.category,
        )
        self.item_2 = Item.objects.create(
            title=f"Test item 2",
            description=f"Test item 2 description",
            price=100,
            category=self.category,
        )

    def setup_session(self):
        self.session = Session.objects.create(session_key="test_session_key",
                                              expire_date=timezone.now() + timezone.timedelta(days=1))
        self.client.cookies[settings.SESSION_COOKIE_NAME] = self.session.session_key

    def test_details(self):
        cart = Cart.objects.create(session_key=self.session, item=self.item_1, count=1)

        response: Response = self.client.get(f"/api/carts/{cart.uuid}/")
        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        self.assertEqual(
            response_data,
            {
                "uuid": str(cart.uuid),
                "item": str(cart.item.uuid),
                "count": cart.count,
            }
        )

    def test_create(self):
        response: Response = self.client.post(f"/api/carts/", data={"item": str(self.item_1.uuid), "count": 1})
        self.assertEqual(response.status_code, 201)

        response_data = response.json()

        self.assertIn("uuid", response_data, response_data)
        self.assertIn("item", response_data, response_data)
        self.assertIn("count", response_data, response_data)

        self.assertEqual(response_data["item"], str(self.item_1.uuid), response_data)
        self.assertEqual(response_data["count"], 1, response_data)

        self.assertEqual(Cart.objects.count(), 1)

        response: Response = self.client.post(
            f"/api/carts/",
            data={
                "item": str(self.item_1.uuid),
                "count": 1
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Cart.objects.count(), 1)

    def test_list(self):
        Cart.objects.create(session_key=self.session, item=self.item_1, count=1)
        Cart.objects.create(session_key=self.session, item=self.item_2, count=1)

        response: Response = self.client.get(f"/api/carts/?limit=1")
        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        self.assertIn("results", response_data, response_data)
        self.assertIn("count", response_data, response_data)

        self.assertEqual(response_data["count"], 2, response_data)
        self.assertNotEqual(response_data["next"], None, response_data)
        self.assertEqual(response_data["previous"], None, response_data)
        self.assertEqual(len(response_data["results"]), 1, response_data)

        response: Response = self.client.get(response_data["next"])
        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        self.assertIn("results", response_data, response_data)
        self.assertIn("count", response_data, response_data)
        self.assertEqual(response_data["count"], 2, response_data)
        self.assertNotEqual(response_data["previous"], None, response_data)
        self.assertEqual(response_data["next"], None, response_data)
        self.assertEqual(len(response_data["results"]), 1, response_data)

    def test_delete(self):
        cart = Cart.objects.create(session_key=self.session, item=self.item_1, count=1)

        self.assertEqual(Cart.objects.count(), 1)
        response: Response = self.client.delete(f"/api/carts/{cart.uuid}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Cart.objects.count(), 0)
