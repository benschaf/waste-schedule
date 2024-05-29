from django.test import TestCase
from django.urls import reverse

class LandingPageTest(TestCase):
    def test_landing_page_status_code(self):
        response = self.client.get(reverse('landing_page'))
        self.assertEqual(response.status_code, 200)

    def test_landing_page_template(self):
        response = self.client.get(reverse('landing_page'))
        self.assertTemplateUsed(response, 'core/index.html')


class AboutPageTest(TestCase):
    def test_about_page_status_code(self):
        response = self.client.get(reverse('about_page'))
        self.assertEqual(response.status_code, 200)

    def test_about_page_template(self):
        response = self.client.get(reverse('about_page'))
        self.assertTemplateUsed(response, 'core/about.html')