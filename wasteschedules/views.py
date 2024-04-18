from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Schedule, Location, Comment, Like, Subscription

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
    template_name = 'wasteschedules/schedule_list.html'
    queryset = Schedule.objects.all()

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
        # Maybe use comments to show one single comment at the top like for example under a youtube video
        context["comments"] = Comment.objects.filter(schedule_id=self.object.id)
        context["like_count"] = Like.objects.filter(schedule_id=self.object.id).count()
        context["is_liked"] = Like.objects.filter(schedule_id=self.object.id, liked_by=self.request.user.id).exists()
        context["is_subscribed"] = Subscription.objects.filter(schedule_id=self.object.id, subscribed_by=self.request.user.id).exists()


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
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in additional Query Sets
        context["comments"] = Comment.objects.filter(schedule_id=self.object.id)
        context["like_count"] = Like.objects.filter(schedule_id=self.object.id).count()
        # -> Credit for checking wether a queryset contains any items: https://docs.djangoproject.com/en/5.0/ref/models/querysets/#django.db.models.query.QuerySet.exists
        # -> Credit for authenticating the logged in user: https://docs.djangoproject.com/en/5.0/topics/auth/default/#authentication-in-web-requests
        context["is_liked"] = Like.objects.filter(schedule_id=self.object.id, liked_by=self.request.user.id).exists()
        context["is_subscribed"] = Subscription.objects.filter(schedule_id=self.object.id, subscribed_by=self.request.user.id).exists()
        return context
