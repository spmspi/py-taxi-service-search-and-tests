from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

URL_DRIVER_URL = reverse("taxi:driver-list")
URL_MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicTaxiTest(TestCase):

    def test_login_required(self):
        res = self.client.get(URL_DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTaxiTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            first_name="test",
            last_name="test",
            username="test",
            email="test@test.tes",
            password="Test123",
            license_number="TES12345",
        )
        self.client.force_login(self.user)

        self.man1 = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.man2 = Manufacturer.objects.create(name="BMW", country="Germany")

    def test_driver_list(self):
        response = self.client.get(URL_DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_manufacturer(self):
        res = URL_MANUFACTURER_URL
        response = self.client.get(res, {"name": "toy"})
        self.assertEqual(response.status_code, 200)
