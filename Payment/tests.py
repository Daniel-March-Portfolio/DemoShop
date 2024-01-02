from unittest.mock import patch

from django.conf import settings
from django.contrib.sessions.models import Session
from django.test import TestCase
from django.utils import timezone
from requests import Response

from Category.models import Category
from Item.models import Item
from Payment.models import Payment, PAYMENT_STATUSES, PaymentItem


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
        payment = Payment.objects.create(client_secret="", session_key=self.session, status=PAYMENT_STATUSES.waiting)
        payment_item = PaymentItem.objects.create(payment=payment, item=self.item_1, count=1)

        response: Response = self.client.get(f"/api/payments/{payment.uuid}/")
        self.assertEqual(response.status_code, 200, response.content)

        response_data = response.json()

        self.assertEqual(
            response_data,
            {
                "uuid": str(payment.uuid),
                "client_secret": payment.client_secret,
                "status": payment.status,
                "items": [
                    {
                        "uuid": str(payment_item.uuid),
                        "item": str(payment_item.item.uuid),
                        "count": 1
                    }
                ],
            }
        )

    @patch("Payment.tasks.create_payment_intent.delay")
    def test_create(self, create_payment_intent):
        response: Response = self.client.post("/api/payments/",
                                              data={"items": [{"item": str(self.item_1.uuid), "count": 1}]},
                                              content_type="application/json")
        self.assertEqual(response.status_code, 201, response.content)

        response_data = response.json()

        self.assertIn("uuid", response_data, response_data)
        self.assertIn("client_secret", response_data, response_data)
        self.assertIn("status", response_data, response_data)
        self.assertIn("items", response_data, response_data)

        self.assertEqual(response_data["status"], PAYMENT_STATUSES.created, response_data)
        self.assertEqual(len(response_data["items"]), 1, response_data)
        self.assertEqual(response_data["items"][0]["item"], str(self.item_1.uuid), response_data)

        self.assertEqual(Payment.objects.count(), 1)
        self.assertTrue(create_payment_intent.called)

    def test_list(self):
        Payment.objects.create(client_secret="", session_key=self.session, status=PAYMENT_STATUSES.waiting)
        Payment.objects.create(client_secret="", session_key=self.session, status=PAYMENT_STATUSES.waiting)

        response: Response = self.client.get(f"/api/payments/?limit=1")
        self.assertEqual(response.status_code, 200, response.content)

        response_data = response.json()

        self.assertIn("results", response_data, response_data)
        self.assertIn("count", response_data, response_data)

        self.assertEqual(response_data["count"], 2, response_data)
        self.assertNotEqual(response_data["next"], None, response_data)
        self.assertEqual(response_data["previous"], None, response_data)
        self.assertEqual(len(response_data["results"]), 1, response_data)

        response: Response = self.client.get(response_data["next"])
        self.assertEqual(response.status_code, 200, response.content)

        response_data = response.json()

        self.assertIn("results", response_data, response_data)
        self.assertIn("count", response_data, response_data)
        self.assertEqual(response_data["count"], 2, response_data)
        self.assertNotEqual(response_data["previous"], None, response_data)
        self.assertEqual(response_data["next"], None, response_data)
        self.assertEqual(len(response_data["results"]), 1, response_data)
