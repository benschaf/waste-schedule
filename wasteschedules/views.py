import json
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from schedulebuilder.views import _event_to_json
from schedulebuilder.models import Event
from .models import Schedule, Location, Comment, Like, Subscription
from .forms import CommentForm

# Create your views here.
# -> Credit for class based views: https://docs.djangoproject.com/en/5.0/ref/class-based-views/


class ScheduleList(ListView):
    """
    A view that displays a list of schedules.

    Attributes:
        template_name (str): The name of the template to be used.
        queryset (QuerySet): The queryset to be used.

    Methods:
        get_context_data: Adds additional context data to the view.
    """
    model = Schedule
    template_name = 'wasteschedules/schedule_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        # -> Credit for getting positional arguments within the get queryset function: https://docs.djangoproject.com/en/5.0/topics/class-based-views/generic-display/#dynamic-filtering
        postcode = self.kwargs['postcode']
        queryset = queryset.filter(locations=postcode)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the view.

        Additional context data:

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
class ScheduleComment(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['body']
    login_url = '/accounts/login/'

    def form_valid(self, form):
        form.instance.commented_by = self.request.user
        slug = self.kwargs.get('slug')
        form.instance.schedule_id = get_object_or_404(Schedule, slug=slug)
        return super().form_valid(form)


# -> Credit for edit view: https://github.com/Code-Institute-Solutions/blog/tree/main/12_views_part_3/05_edit_delete
def schedule_comment_edit(request, pk, slug):
    """
    view to edit comments
    """
    if request.method == "POST":

        comment = get_object_or_404(Comment, pk=pk)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.commented_by == request.user:
            comment = comment_form.save(commit=False)
            comment.save()

    postcode = comment.schedule_id.locations.all()[0]
    return HttpResponseRedirect(reverse('schedule_detail', kwargs={'postcode' : postcode, 'slug': slug}))


class ScheduleCommentDelete(DeleteView):
    model = Comment

# i am not sure if this works correctly
    def get_object(self):
        obj = super().get_object(queryset=None)
        if not obj.commented_by == self.request.user:
            raise Http404("You're not the owner of this comment.")
        return obj

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', reverse_lazy('wasteschedules/'))


class ScheduleLike(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def post(self, request, slug):
        schedule = get_object_or_404(Schedule, slug=slug)
        # -> Credit for creating an object: https://docs.djangoproject.com/en/5.0/topics/db/queries/#creating-objects
        # -> Credit for deleting an object: https://docs.djangoproject.com/en/5.0/topics/db/queries/#deleting-objects
        # -> Credit for checking if an object exists: https://docs.djangoproject.com/en/5.0/ref/models/querysets/#exists
        if not Like.objects.filter(schedule_id=schedule.id, liked_by=request.user.id).exists():
            l = Like(schedule_id=schedule, liked_by=request.user)
            l.save()
        else:
            Like.objects.filter(schedule_id=schedule.id,
                                liked_by=request.user.id).delete()
        return redirect(request.META.get('HTTP_REFERER', 'wasteschedules/'))


class ScheduleSubscribe(View):
    def post(self, request, slug):
        schedule = get_object_or_404(Schedule, slug=slug)
        if not Subscription.objects.filter(schedule_id=schedule.id, subscribed_by=request.user.id).exists():
            s = Subscription(schedule_id=schedule, subscribed_by=request.user)
            s.save()
        else:
            Subscription.objects.filter(
                schedule_id=schedule.id, subscribed_by=request.user.id).delete()
        return redirect(request.META.get('HTTP_REFERER', 'wasteschedules/'))
