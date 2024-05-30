from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from wasteschedules.models import PostalCode, Schedule
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


class CreateScheduleTestCase(TestCase):
    """
    Test case for the CreateSchedule view.
    """

    def setUp(self):
        """
        Set up the necessary objects and data for the test case.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.postal_code = PostalCode.objects.create(postal_code='12345')

    def test_create_schedule_render(self):
        """
        Tests if a schedule can be created by an authenticated user.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('create_schedule', kwargs={'postal_code': '12345'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schedulebuilder/schedule_form.html')

    def test_create_schedule_post(self):
        """
        Tests if a schedule can be created by an authenticated user.
        """
        self.client.login(username='testuser', password='12345')
        form_data = {
            'title': 'Test Schedule',
            'description': 'This is a test schedule',
            'image': 'test.jpg',
        }
        response = self.client.post(reverse('create_schedule', kwargs={'postal_code': '12345'}), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Schedule.objects.filter(title='Test Schedule').exists())

    def test_create_schedule_unauthenticated(self):
        """
        Tests if an unauthenticated user is redirected to the login page.
        """
        response = self.client.get(reverse('create_schedule', kwargs={'postal_code': '12345'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/schedule-builder/title-description/12345')


    def test_create_schedule_empty_title(self):
        """
        Tests if the form is invalid when required fields are missing.
        """
        self.client.login(username='testuser', password='12345')
        form_data = {
            'title': '',
        }
        response = self.client.post(reverse('create_schedule', kwargs={'postal_code': '12345'}), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Schedule.objects.filter(title='').exists())


class UpdateScheduleTestCase(TestCase):
    """
    Test case for the UpdateSchedule view.
    """

    def setUp(self):
        """
        Set up the necessary objects and data for the test case.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.schedule = Schedule.objects.create(
            title='test schedule',
            author=self.user,
        )

    def test_update_schedule(self):
        """
        Tests if a schedule can be successfully updated.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('edit_schedule', kwargs={'slug': self.schedule.slug}), {
            'description': 'Updated description',
            'image': 'updated_image.jpg',
        })
        self.assertEqual(response.status_code, 302)
        self.schedule.refresh_from_db()
        self.assertEqual(self.schedule.description, 'Updated description')
        self.assertNotEqual(self.schedule.image, 'placeholder')

    def test_update_schedule_unauthenticated(self):
        """
        Tests if an unauthenticated user is redirected to the login page when trying to update a schedule.
        """
        response = self.client.post(reverse('edit_schedule', kwargs={'slug': self.schedule.slug}), {
            'description': 'Updated description',
            'image': 'updated_image.jpg',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/')

    def test_update_schedule_wrong_user(self):
        """
        Tests if a user cannot update another user's schedule.
        """
        self.user2 = User.objects.create_user(username='anotheruser', password='12345')
        self.client.login(username='anotheruser', password='12345')
        response = self.client.post(reverse('edit_schedule', kwargs={'slug': self.schedule.slug}), {
            'description': 'Updated description',
            'image': 'updated_image.jpg',
        })
        self.assertEqual(response.status_code, 302)
        self.schedule.refresh_from_db()
        self.assertNotEqual(self.schedule.description, 'Updated description')
        self.assertNotEqual(self.schedule.image, 'updated_image.jpg')