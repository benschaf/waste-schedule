from django.shortcuts import render
from django.views.generic import ListView
from .models import Schedule

# Create your views here.
class ScheduleList(ListView):
    """
    A view that displays a list of schedules.
    """
    model = Schedule
    template_name = 'wasteschedules/schedule_list.html'
    paginate_by = 10
    queryset = Schedule.objects.all()