from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from wasteschedules.models import PostalCode
from schedulebuilder.forms import PostalCodeForm
from django.contrib.messages import get_messages


class PickLocationTestCase(TestCase):
    """
    Test case for the PickLocation view.
    """

    def setUp(self):
        """
        Set up the necessary objects and data for the test case.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345')

    def test_pick_location_view_rendered(self):
        """
        Tests if the pick location form is displayed.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('pick_location'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schedulebuilder/location_form.html')
        self.assertIsInstance(response.context['form'], PostalCodeForm)

    def test_pick_location_existing_location(self):
        """
        Tests if the form submission for an existing location redirects to the create_schedule view.
        """
        self.client.login(username='testuser', password='12345')
        PostalCode.objects.create(postal_code='12345')
        response = self.client.post(reverse('pick_location'), {
                                    'postal_code': '12345'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'create_schedule', kwargs={'postal_code': '12345'}))

    def test_pick_location_new_location(self):
        """
        Tests if the form submission for a new location redirects to the create_schedule view.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('pick_location'), {
                                    'postal_code': '12345'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'create_schedule', kwargs={'postal_code': '12345'}))

    # -> Credit for getting django messages from response: https://stackoverflow.com/questions/2897609/how-can-i-unit-test-django-messages
    def test_pick_location_form_submission_existing_location_message(self):
        """
        Tests if a message is displayed when submitting the form for an existing location.
        """
        self.client.login(username='testuser', password='12345')
        PostalCode.objects.create(postal_code='12345')
        response = self.client.post(reverse('pick_location'), {
                                    'postal_code': '12345'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(
            messages[0]), "Your Location already exists. Check out if there already is a schedule for it.")

    def test_pick_location_form_submission_invalid_form(self):
        """
        Tests if an invalid form submission displays the form again.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('pick_location'), {'postal_code': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schedulebuilder/location_form.html')
        self.assertIsInstance(response.context['form'], PostalCodeForm)
