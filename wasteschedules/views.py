from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Schedule

# Create your views here.
# ->Credit for class based views: https://docs.djangoproject.com/en/5.0/ref/class-based-views/
class ScheduleList(ListView):
    """
    A view that displays a list of schedules.
    """
    template_name = 'wasteschedules/schedule_list.html'
    queryset = Schedule.objects.all()

class ScheduleDetail(DetailView):
    """
    A view that displays a single schedule.
    """
    template_name = 'wasteschedules/schedule_detail.html'
    model = Schedule
