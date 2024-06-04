from ics import Calendar, Event as IcsEvent
import json
from typing import Any
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView
from schedulebuilder.views import _event_to_json
from schedulebuilder.models import Event
from .models import Schedule, Comment, Like, Subscription, PostalCode
from .forms import CommentForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

# Create your views here.
# -> Credit for class based views: https://docs.djangoproject.com/en/5.0/ref/class-based-views/


class ScheduleList(ListView):
    """
    A view that displays a list of schedules.

    Attributes:
        model (Model): The model to be used for the queryset.
        template_name (str): The name of the template to be used.

    Methods:
        get_queryset: Returns the queryset to be used for the view.
        get_context_data: Adds additional context data to the view.
    """
    model = Schedule
    template_name = 'wasteschedules/schedule_list.html'

    def get_queryset(self):
        """
        Returns the queryset to be used for the view.

        If a valid postcode is provided, filters the queryset based on the locations associated with the postcode.

        Returns:
            QuerySet: The filtered queryset.
        """
        queryset = super().get_queryset()
        postcode = self.kwargs['postcode']
        if postcode != '0':
            postcode_obj = None
            try:
                postcode_obj = PostalCode.objects.get(postal_code=postcode)
            except PostalCode.DoesNotExist:
                postcode_obj = None
            queryset = queryset.filter(locations=postcode_obj)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the view.

        Additional context data:
        - schedule_list: The list of schedules annotated with the count of likes.
        - user_likes: The list of schedule IDs liked by the current user.
        - user_subscriptions: The list of schedule IDs subscribed by the current user.
        - postcode: The postcode associated with the view.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        # Maybe use comments to show one single comment at the top like for example under a youtube video
        # -> Credit for adding an annotation to each object in a list: https://docs.djangoproject.com/en/5.0/topics/db/aggregation/
        context["schedule_list"] = context["schedule_list"].annotate(
            Count('like'))
        # -> Credit for passing only the id field value to the template: https://docs.djangoproject.com/en/5.0/ref/models/querysets/#values-list
        context["user_likes"] = Like.objects.filter(
            liked_by=self.request.user.id).values_list('schedule_id', flat=True)
        context["user_subscriptions"] = Subscription.objects.filter(
            subscribed_by=self.request.user.id).values_list('schedule_id', flat=True)
        context["postcode"] = self.kwargs['postcode']
        return context


class ScheduleDetail(DetailView):
    """
    A view that displays a single schedule.

    Attributes:
        template_name (str): The name of the template to be used.
        model (Schedule): The model to be used.

    Methods:
        get_context_data: Adds additional context data to the view.
    """

    template_name = 'wasteschedules/schedule_detail.html'
    model = Schedule

    # -> Credit for additional context data in class based views: https://docs.djangoproject.com/en/5.0/topics/class-based-views/generic-display/
    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the view.

        Additional context data:
            comments (QuerySet): The comments associated with the schedule.
            like_count (int): The number of likes associated with the schedule.
            is_liked (bool): Whether the schedule is liked by the logged in user.
            is_subscribed (bool): Whether the schedule is subscribed to by the logged in user.

        Returns:
            dict: The context data.

        """
        context = super().get_context_data(**kwargs)

        context["comments"] = Comment.objects.filter(
            schedule_id=self.object.id)
        context["like_count"] = Like.objects.filter(
            schedule_id=self.object.id).count()
        # -> Credit for checking wether a queryset contains any items: https://docs.djangoproject.com/en/5.0/ref/models/querysets/#django.db.models.query.QuerySet.exists
        # -> Credit for authenticating the logged in user: https://docs.djangoproject.com/en/5.0/topics/auth/default/#authentication-in-web-requests
        context["is_liked"] = Like.objects.filter(
            schedule_id=self.object.id, liked_by=self.request.user.id).exists()
        context["is_subscribed"] = Subscription.objects.filter(
            schedule_id=self.object.id, subscribed_by=self.request.user.id).exists()
        context["comment_form"] = CommentForm()
        context["location"] = self.kwargs['postcode']

        events = Event.objects.filter(schedule_id=self.object.id)
        context["event_data"] = json.dumps(_event_to_json(events))
        return context


# -> Credit for using the LoginRequiredMixin: https://docs.djangoproject.com/en/5.0/topics/auth/default/#the-loginrequiredmixin-mixin
class ScheduleComment(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    A view for creating comments on a schedule.

    Inherits from LoginRequiredMixin, SuccessMessageMixin, and CreateView.
    """

    model = Comment
    fields = ['body']
    login_url = '/accounts/login/'
    success_message = "Your Comment was created successfully."

    def form_valid(self, form):
        form.instance.commented_by = self.request.user
        slug = self.kwargs.get('slug')
        form.instance.schedule_id = get_object_or_404(Schedule, slug=slug)
        return super().form_valid(form)

    # -> Credit for finding class based view methods: https://www.brennantymrak.com/articles/createviewdiagram
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        if form.instance.body == "":
            messages.add_message(self.request, messages.ERROR,
                                 "Your comment cannot be empty.")
            return redirect(self.request.META.get('HTTP_REFERER', 'landing_page'))
        return super().form_invalid(form)


# -> Credit for edit view: https://github.com/Code-Institute-Solutions/blog/tree/main/12_views_part_3/05_edit_delete
def schedule_comment_edit(request, pk, slug):
    """
    View to edit comments.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the comment to be edited.
        slug (str): The slug of the schedule.

    Returns:
        HttpResponseRedirect: Redirects to the schedule detail page.

    Notes:
        - This view expects a POST request to edit the comment.
        - If the comment does not belong to the current user, a Django message with an error is added.
        - If the comment is successfully edited, a Django message with a success message is added.
        - After editing the comment, the user is redirected to the schedule detail page.

    """
    if request.method == "POST":

        comment = get_object_or_404(Comment, pk=pk)
        if comment.commented_by != request.user:
            # instead of the response forbidden add a django message - and then delete return redirect to url that makes sense
            messages.add_message(request, messages.ERROR,
                                 "You are not the owner of this comment.")
            return redirect(request.META.get('HTTP_REFERER', 'landing_page'))

        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.commented_by == request.user:
            comment = comment_form.save(commit=False)
            comment.edited = True
            messages.add_message(request, messages.INFO,
                                 "Your comment was edited successfully.")
            comment.save()
    # Do I need an else here to handle get? I am never expecting a get request for this

    postcode = comment.schedule_id.locations.all()[0]
    return HttpResponseRedirect(reverse('schedule_detail', kwargs={'postcode': postcode, 'slug': slug}))


class ScheduleCommentDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    A view for deleting a comment from the schedule.

    Inherits from LoginRequiredMixin, SuccessMessageMixin, and DeleteView.
    """

    model = Comment
    success_message = "Your comment was deleted successfully."

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        obj = self.get_object()
        if not obj.commented_by == self.request.user:
            messages.add_message(self.request, messages.ERROR,
                                 "You are not the owner of this comment.")
            return redirect(self.request.META.get('HTTP_REFERER', 'landing_page'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """
        Get the URL to redirect to after the comment is successfully deleted.

        Returns:
            Redirects to the landing page
        """
        return self.request.META.get('HTTP_REFERER', reverse_lazy('landing_page'))


class ScheduleLike(LoginRequiredMixin, View):
    """
    Handles the liking and unliking of a schedule by a user.
    """

    login_url = '/accounts/login/'

    def post(self, request, slug):
        """
        Handle the HTTP POST request for liking or removing a like from a schedule.

        Args:
            request (HttpRequest): The HTTP request object.
            slug (str): The slug of the schedule.

        Returns:
            HttpResponseRedirect: A redirect response to the previous page.

        Raises:
            Http404: If the schedule with the given slug does not exist.

        """
        schedule = get_object_or_404(Schedule, slug=slug)
        # -> Credit for creating an object: https://docs.djangoproject.com/en/5.0/topics/db/queries/#creating-objects
        # -> Credit for deleting an object: https://docs.djangoproject.com/en/5.0/topics/db/queries/#deleting-objects
        # -> Credit for checking if an object exists: https://docs.djangoproject.com/en/5.0/ref/models/querysets/#exists
        if not Like.objects.filter(schedule_id=schedule.id, liked_by=request.user.id).exists():
            l = Like(schedule_id=schedule, liked_by=request.user)
            l.save()
            messages.add_message(self.request, messages.SUCCESS,
                                 f"Successfully liked {schedule}")
        else:
            Like.objects.filter(schedule_id=schedule.id,
                                liked_by=request.user.id).delete()
            messages.add_message(self.request, messages.SUCCESS,
                                 f"Successfully removed like from {schedule}")
        return redirect(request.META.get('HTTP_REFERER', 'landing_page'))


class ScheduleSubscribe(LoginRequiredMixin, View):
    """
    View class for subscribing or unsubscribing to a schedule.

    Methods:
    - post(request, slug): Handles the POST request for subscribing or unsubscribing to a schedule.
    """

    def post(self, request, slug):
        """
        Handle the HTTP POST request for subscribing/unsubscribing to a schedule.

        Args:
            request (HttpRequest): The HTTP request object.
            slug (str): The slug of the schedule.

        Returns:
            HttpResponseRedirect: A redirect response to the previous page.

        Raises:
            None

        """
        schedule = get_object_or_404(Schedule, slug=slug)
        if not Subscription.objects.filter(schedule_id=schedule.id, subscribed_by=request.user.id).exists():
            s = Subscription(schedule_id=schedule, subscribed_by=request.user)
            s.save()
            messages.add_message(self.request, messages.SUCCESS,
                                 f"Successfully subscribed to {schedule}")
        else:
            Subscription.objects.filter(
                schedule_id=schedule.id, subscribed_by=request.user.id).delete()
            messages.add_message(self.request, messages.SUCCESS,
                                 f"Successfully unsubscribed from {schedule}")

        return redirect(request.META.get('HTTP_REFERER', 'wasteschedules/'))


class Dashboard(LoginRequiredMixin, TemplateView):
    """
    A view class representing the dashboard page.

    This view displays the dashboard page, which includes information about the user's subscribed schedules
    and schedules they own.

    Attributes:
        template_name (str): The name of the template used to render the dashboard page.

    Methods:
        get_context_data(**kwargs): Retrieves the context data for rendering the dashboard page.

    """

    template_name = 'wasteschedules/dashboard.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Retrieves the context data for rendering the dashboard page.

        Additional context data:
        - user: The current user.
        - subscribed_schedules: The schedules subscribed to by the current user.
        - owned_schedules: The schedules owned by the current user.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict[str, Any]: The context data for rendering the dashboard page.

        """
        context = super().get_context_data(**kwargs)

        # is it safe to add the user to the context like this?
        context['user'] = self.request.user
        context['subscribed_schedules'] = Schedule.objects.filter(
            subscription__subscribed_by=self.request.user)
        context['owned_schedules'] = Schedule.objects.filter(
            author=self.request.user)

        return context


def download_ics(request, id):
    # -> Credit for ics.py library that helps to create ics files: https://icspy.readthedocs.io/en/stable
    # I cannot add the rrule properties to the event because ics.py does not support it yet: https://icspy.readthedocs.io/en/stable/misc.html#missing-support-for-recurrent-events
    c = Calendar()

    schedule_events = Event.objects.filter(schedule_id=id)
    for db_event in schedule_events:
        e = IcsEvent()
        e.name = db_event.get_kind_display()
        e.description = db_event.get_kind_display()
        e.location = "right on your doorstep"
        e.begin = db_event.date
        e.created = db_event.created_on
        e.make_all_day()
        c.events.add(e)

    # -> Credit for creating a download response: https://docs.djangoproject.com/en/5.0/ref/request-response/#fileresponse-objects
    response = HttpResponse(str(c.serialize()), content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename="events.ics"'

    return response
