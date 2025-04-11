from django.test import TestCase, Client
from django.urls import reverse

class DashboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_dashboard_home_status_code(self):
        url = reverse('dashboard_home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_home_content(self):
        url = reverse('dashboard_home')
        response = self.client.get(url)
        self.assertContains(response, "Retail Inventory Optimization Dashboard")
