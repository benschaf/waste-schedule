from django.test import TestCase
from django.urls import reverse


class LandingPageTest(TestCase):
    """
    Test case for the landing page view.
    """

    def test_landing_page_status_code(self):
        """
        Test if the landing page returns a status code of 200.
        """
        response = self.client.get(reverse('landing_page'))
        self.assertEqual(response.status_code, 200)

    def test_landing_page_template(self):
        """
        Test if the landing page uses the correct template.
        """
        response = self.client.get(reverse('landing_page'))
        self.assertTemplateUsed(response, 'core/index.html')


class AboutPageTest(TestCase):
    """
    Test case for the about page view.
    """

    def test_about_page_status_code(self):
        """
        Test if the about page returns a status code of 200.
        """
        response = self.client.get(reverse('about_page'))
        self.assertEqual(response.status_code, 200)

    def test_about_page_template(self):
        """
        Test if the about page uses the correct template.
        """
        response = self.client.get(reverse('about_page'))
        self.assertTemplateUsed(response, 'core/about.html')
