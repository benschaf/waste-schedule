from datetime import datetime
from django.http import JsonResponse
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from schedulebuilder.models import Event
from schedulebuilder.views import EditCalendarView
from schedulebuilder.forms import PostalCodeForm
from wasteschedules.models import PostalCode, Schedule


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
        Tests if the form submission for an existing location redirects to the
        create_schedule view.
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
        Tests if the form submission for a new location redirects to the
        create_schedule view.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('pick_location'), {
                                    'postal_code': '12345'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'create_schedule', kwargs={'postal_code': '12345'}))

    # -> Credit for getting django messages from response: https://stackoverflow.com/questions/2897609/how-can-i-unit-test-django-messages  # noqa
    def test_pick_location_form_submission_existing_location_message(self):
        """
        Tests if a message is displayed when submitting the form for an
        existing location.
        """
        self.client.login(username='testuser', password='12345')
        PostalCode.objects.create(postal_code='12345')
        response = self.client.post(reverse('pick_location'), {
                                    'postal_code': '12345'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(
            messages[0]), "Your Location already exists. Check out if there "
            "already is a schedule for it.")

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
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        self.postal_code = PostalCode.objects.create(postal_code='12345')

    def test_create_schedule_render(self):
        """
        Tests if a schedule can be created by an authenticated user.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('create_schedule',
                                           kwargs={'postal_code': '12345'}))
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
        response = self.client.post(
            reverse(
                "create_schedule", kwargs={"postal_code": "12345"}), form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Schedule.objects.filter(title='Test Schedule').exists())

    def test_create_schedule_unauthenticated(self):
        """
        Tests if an unauthenticated user is redirected to the login page.
        """
        response = self.client.get(reverse('create_schedule',
                                           kwargs={'postal_code': '12345'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '/accounts/login/?next=/schedule-builder/title-description/12345')

    def test_create_schedule_empty_title(self):
        """
        Tests if the form is invalid when required fields are missing.
        """
        self.client.login(username='testuser', password='12345')
        form_data = {
            'title': '',
        }
        response = self.client.post(
            reverse('create_schedule', kwargs={'postal_code': '12345'}),
            form_data)
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
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        self.schedule = Schedule.objects.create(
            title='test schedule',
            author=self.user,
        )

    def test_update_schedule(self):
        """
        Tests if a schedule can be successfully updated.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse("edit_schedule", kwargs={"slug": self.schedule.slug}),
            {
                "description": "Updated description",
                "image": "updated_image.jpg",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.schedule.refresh_from_db()
        self.assertEqual(self.schedule.description, 'Updated description')
        self.assertNotEqual(self.schedule.image, 'placeholder')

    def test_update_schedule_unauthenticated(self):
        """
        Tests if an unauthenticated user is redirected to the login page when
        trying to update a schedule.
        """
        response = self.client.post(
            reverse("edit_schedule", kwargs={"slug": self.schedule.slug}),
            {
                "description": "Updated description",
                "image": "updated_image.jpg",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/')

    def test_update_schedule_wrong_user(self):
        """
        Tests if a user cannot update another user's schedule.
        """
        self.user2 = User.objects.create_user(
            username='anotheruser', password='12345')
        self.client.login(username='anotheruser', password='12345')
        response = self.client.post(
            reverse("edit_schedule", kwargs={"slug": self.schedule.slug}),
            {
                "description": "Updated description",
                "image": "updated_image.jpg",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.schedule.refresh_from_db()
        self.assertNotEqual(self.schedule.description, 'Updated description')
        self.assertNotEqual(self.schedule.image, 'updated_image.jpg')


class DeleteScheduleTestCase(TestCase):
    """
    Test case for the DeleteSchedule view.
    """

    def setUp(self):
        """
        Set up the necessary objects and data for the test case.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.postal_code = PostalCode.objects.create(postal_code='12345')
        self.schedule = Schedule.objects.create(
            title='test schedule',
            author=self.user,
        )
        self.schedule.locations.add(self.postal_code)

    def test_delete_schedule_authenticated_owner(self):
        """
        Tests if an authenticated owner can delete a schedule.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('delete_schedule', kwargs={'slug': self.schedule.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Schedule.objects.filter(id=self.schedule.id).exists())

    def test_delete_schedule_authenticated_wrong_user(self):
        """
        Tests if an authenticated but wrong user (non-owner) cannot delete a
        schedule.
        """
        User.objects.create_user(username='anotheruser', password='12345')
        self.client.login(username='anotheruser', password='12345')
        response = self.client.post(
            reverse('delete_schedule', kwargs={'slug': self.schedule.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Schedule.objects.filter(id=self.schedule.id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), "You are not the owner of this schedule.")

    def test_delete_schedule_unauthenticated(self):
        """
        Tests if an unauthenticated user cannot delete a schedule.
        """
        response = self.client.post(
            reverse('delete_schedule', kwargs={'slug': self.schedule.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Schedule.objects.filter(id=self.schedule.id).exists())

    def test_delete_schedule_redirect(self):
        """
        Tests if the view redirects to the schedule list page after deleting
        the schedule.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('delete_schedule', kwargs={'slug': self.schedule.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse(
                'schedule_list',
                kwargs={'postcode': self.postal_code.postal_code}))


class EditCalendarViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="12345")
        self.postal_code = PostalCode.objects.create(postal_code='12345')
        self.schedule = Schedule.objects.create(
            title='test schedule',
            author=self.user,
        )
        self.schedule.locations.add(self.postal_code)
        self.event = Event.objects.create(
            js_event_id='1',
            schedule_id=self.schedule,
            kind=0,
            date=datetime.now(),
        )

    def test_dispatch_user_not_owner(self):
        self.user2 = User.objects.create_user(
            username='anotheruser', password='12345')
        self.client.login(username='anotheruser', password='12345')
        response = self.client.get(
            reverse('add_bins', kwargs={'schedule_id': self.schedule.id}))
        self.assertEqual(response.status_code, 302)
        # tests if the user is redirected to the home page
        # (HTTP_REFERER not tested)
        self.assertRedirects(response, '/')

    def test_dispatch_user_owner(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(
            reverse("add_bins", kwargs={"schedule_id": self.schedule.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schedulebuilder/calendar.html')

    def test_get_context_data(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(
            reverse("add_bins", kwargs={"schedule_id": self.schedule.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["schedule"], self.schedule)
        self.assertEqual(
            response.context["postal_code"], self.postal_code.postal_code)
        # i dont know how to test for the json data

    def test_post_valid_json(self):
        self.client.login(username='testuser', password='12345')
        # dont know how to test for the json data

    def test_post_invalid_json(self):
        self.client.login(username='testuser', password='12345')
        data = 'invalid json'
        response = self.client.post(
            reverse("add_bins", kwargs={"schedule_id": self.schedule.id}),
            data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.json(), {'message': 'Invalid JSON'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)

    def test_convert_kind_to_int(self):
        view = EditCalendarView()
        self.assertEqual(view._convert_kind_to_int('Restmüll'), 0)
        self.assertEqual(view._convert_kind_to_int('Biomüll'), 1)
        self.assertEqual(view._convert_kind_to_int('Papiermüll'), 2)
        self.assertEqual(view._convert_kind_to_int('Gelbe Tonne'), 4)
        self.assertIsNone(view._convert_kind_to_int('Invalid Kind'))

# I also don't know how to test the _event_to_json method
