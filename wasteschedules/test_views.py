from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from wasteschedules.forms import CommentForm
from .models import Schedule, Comment, Like, Subscription, PostalCode

# -> Credit for django test assertions: https://docs.djangoproject.com/en/5.0/topics/testing/tools/#assertions
class ScheduleListTestCase(TestCase):
    """
    Test case for the ScheduleList view.
    """

    def setUp(self):
        """
        Set up the necessary objects and data for the test case.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.postal_code = PostalCode.objects.create(postal_code='12345')
        self.schedule1 = Schedule.objects.create(
            title='test schedule1',
            author=self.user,
        )
        self.schedule1.locations.add(self.postal_code)
        self.schedule2 = Schedule.objects.create(
            title='test schedule2',
            author=self.user,
        )
        self.schedule2.locations.add(self.postal_code)
        self.subscription = Subscription.objects.create(
            subscribed_by=self.user,
            schedule_id=self.schedule2,
        )
        self.like = Like.objects.create(
            liked_by=self.user,
            schedule_id=self.schedule1,
        )

    def test_render_schedule_list_existing_postcode(self):
        """
        Tests if schedules are rendered for an existing postcode.
        """
        response = self.client.get(reverse('schedule_list', kwargs={'postcode': '12345'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test schedule1', response.content)
        self.assertIn(b'test schedule2', response.content)

    def test_render_schedule_list_non_existing_postcode(self):
        """
        Tests if no schedules are rendered for a non-existing postcode.
        """
        response = self.client.get(reverse('schedule_list', kwargs={'postcode': '11111'}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['schedule_list'].exists())

    def test_render_schedule_list_invalid_postcode(self):
        """
        Tests if no schedules are rendered for an invalid postcode.
        """
        response = self.client.get(reverse('schedule_list', kwargs={'postcode': '11'}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['schedule_list'].exists())

    def test_render_schedule_list_0_postcode(self):
        """
        Tests if schedules are rendered for a 0 postcode.
        This should be the case because the 0 postcode is added to the url by the "Browse Locations" link in the Navigation bar and should display all schedules.
        """
        response = self.client.get(reverse('schedule_list', kwargs={'postcode': '0'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['schedule_list'].exists())

    def test_like_context_variable(self):
        """
        Tests if the likes are being annotated to the schedule_list queryset correctly.
        """
        response = self.client.get(reverse('schedule_list', kwargs={'postcode': '12345'}))
        self.assertEqual(response.status_code, 200)
        for schedule in response.context['schedule_list']:
            if schedule.id == self.schedule1.id:
                self.assertEqual(schedule.like__count, 1)
            else:
                self.assertEqual(schedule.like__count, 0)

    def test_user_likes(self):
        """
        Tests if the user_likes context variable is being passed correctly.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('schedule_list', kwargs={'postcode': '12345'}))
        self.assertEqual(response.status_code, 200)
        # -> Credit for converting a QuerySet to a list: https://stackoverflow.com/questions/4424435/how-to-convert-a-django-queryset-to-a-list
        self.assertEqual(list(response.context['user_likes']), [self.schedule1.id])

    def test_user_subscriptions(self):
        """
        Tests if the user_subscriptions context variable is being passed correctly.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('schedule_list', kwargs={'postcode': '12345'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['user_subscriptions']), [self.schedule2.id])

    def test_postcode_context_variable(self):
        """
        Tests if the postcode context variable is being passed correctly.
        """
        response = self.client.get(reverse('schedule_list', kwargs={'postcode': '12345'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['postcode'], '12345')



class ScheduleDetailTestCase(TestCase):
    """
    Test case for the ScheduleDetail view.
    """

    def setUp(self):
        """
        Set up the necessary objects and data for the test case.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.postal_code = PostalCode.objects.create(postal_code='12345')
        self.schedule = Schedule.objects.create(
            title='test schedule',
            author=self.user,
        )
        self.schedule.locations.add(self.postal_code)
        self.comment = Comment.objects.create(
            schedule_id=self.schedule,
            commented_by=self.user,
            body='Test comment',
        )
        self.like = Like.objects.create(
            schedule_id=self.schedule,
            liked_by=self.user,
        )
        self.subscription = Subscription.objects.create(
            schedule_id=self.schedule,
            subscribed_by=self.user,
        )

    def test_render_schedule_detail(self):
        """
        Tests if the schedule detail is rendered correctly.
        """
        response = self.client.get(reverse('schedule_detail', kwargs={'postcode': '12345', 'slug': self.schedule.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wasteschedules/schedule_detail.html')
        self.assertIn(b'test schedule', response.content)
        self.assertIn(b'Test comment', response.content)

    def test_schedule_detail_context_variables(self):
        """
        This method tests the context variables returned by the ScheduleDetail view.
        It checks if the correct variables are set in the response context and if their values are as expected.
        """

        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('schedule_detail', kwargs={'postcode': '12345', 'slug': self.schedule.slug}))

        self.assertEqual(response.context['object'], self.schedule)
        self.assertEqual(list(response.context['comments']), [self.comment])
        self.assertEqual(response.context['like_count'], 1)
        self.assertTrue(response.context['is_liked'])
        self.assertTrue(response.context['is_subscribed'])
        self.assertIsInstance(response.context['comment_form'], CommentForm)
        self.assertEqual(response.context['location'], '12345')
        self.assertContains(response, 'Test comment')


class ScheduleCommentTestCase(TestCase):
    """
    Test case for the ScheduleComment view.
    """

    def setUp(self):
        """
        Set up the necessary objects and data for the test case.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.schedule = Schedule.objects.create(
            title='test schedule',
            author=self.user,
        )
        self.schedule.locations.add(PostalCode.objects.create(postal_code='12345'))

    def test_comment_submission_while_logged_out(self):
        """
        This test verifies that when a user is logged out and tries to submit a comment,
        the comment is not saved and the response status code is 302 (redirect).
        """
        post_data = {
            'body': 'Test comment',
        }
        self.client.logout()
        response = self.client.post(reverse('schedule_comment', kwargs={'slug': self.schedule.slug}), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(body='Test comment').exists())

    def test_successful_comment_submission(self):
        """
        Tests if a comment is successfully submitted.
        """
        post_data = {
            'body': 'Test comment',
        }
        response = self.client.post(reverse('schedule_comment', kwargs={'slug': self.schedule.slug}), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(body='Test comment').exists())

    def test_empty_comment_submission(self):
        """
        Tests if a comment is not submitted if it is empty.
        """
        post_data = {
            'body': '',
        }
        response = self.client.post(reverse('schedule_comment', kwargs={'slug': self.schedule.slug}), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(body='').exists())


class ScheduleCommentEditTestCase(TestCase):
    """
    Test case for the schedule_comment_edit view.
    """

    def setUp(self):
        """
        Set up the necessary objects and data for the test case.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.postal_code = PostalCode.objects.create(postal_code='12345')
        self.schedule = Schedule.objects.create(
            title='test schedule',
            author=self.user,
        )
        self.schedule.locations.add(self.postal_code)
        self.comment = Comment.objects.create(
            schedule_id=self.schedule,
            commented_by=self.user,
            body='Test comment',
        )

    def test_schedule_comment_edit(self):
        """
        Tests if the comment is successfully edited.
        """
        self.client.login(username='testuser', password='12345')
        new_comment_body = 'Updated comment'
        response = self.client.post(reverse('schedule_comment_update', kwargs={'pk': self.comment.pk, 'slug': self.schedule.slug}), {'body': new_comment_body})
        self.assertEqual(response.status_code, 302)
        # -> Credit for refreshing the object from the database: https://stackoverflow.com/questions/4377861/reload-django-object-from-database
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.body, new_comment_body)

    def test_schedule_comment_edit_unauthorized(self):
        """
        Tests if an unauthorized user is prevented from editing the comment.
        """
        self.client.login(username='unauthorized', password='12345')
        new_comment_body = 'Updated comment'
        response = self.client.post(reverse('schedule_comment_update', kwargs={'pk': self.comment.pk, 'slug': self.schedule.slug}), {'body': new_comment_body})
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertNotEqual(self.comment.body, new_comment_body)

    def test_schedule_comment_edit_empty_comment(self):
        """
        Tests if an empty comment is not allowed.
        """
        self.client.login(username='testuser', password='12345')
        new_comment_body = ''
        response = self.client.post(reverse('schedule_comment_update', kwargs={'pk': self.comment.pk, 'slug': self.schedule.slug}), {'body': new_comment_body})
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertNotEqual(self.comment.body, new_comment_body)

    def test_schedule_comment_edit_wrong_user(self):
        """
        Tests if a user cannot edit another user's comment.
        """
        self.user2 = User.objects.create_user(username='anotheruser', password='12345')
        self.client.login(username='anotheruser', password='12345')
        new_comment_body = 'Updated comment'
        response = self.client.post(reverse('schedule_comment_update', kwargs={'pk': self.comment.pk, 'slug': self.schedule.slug}), {'body': new_comment_body})
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertNotEqual(self.comment.body, new_comment_body)


class ScheduleCommentDeleteTestCase(TestCase):
    """
    Test case for the ScheduleCommentDelete view.
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
        self.comment = Comment.objects.create(
            schedule_id=self.schedule,
            commented_by=self.user,
            body='Test comment',
        )

    def test_delete_comment(self):
        """
        Tests if the comment is successfully deleted.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('schedule_comment_delete', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_delete_comment_unauthorized(self):
        """
        Tests if an unauthorized user cannot delete the comment.
        """
        self.client.login(username='unauthorized', password='12345')
        response = self.client.post(reverse('schedule_comment_delete', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_delete_comment_wrong_user(self):
        """
        Tests if a user cannot delete another user's comment.
        """
        self.user2 = User.objects.create_user(username='anotheruser', password='12345')
        self.client.login(username='anotheruser', password='12345')
        response = self.client.post(reverse('schedule_comment_delete', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())
