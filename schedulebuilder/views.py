from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from schedulebuilder.forms import *
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Create your views here.


class CreateSchedule(CreateView, LoginRequiredMixin):
    form_class = ScheduleForm
    model = Schedule

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('add_bin', kwargs={'schedule_id': self.object.id})

    # to add the location i will need an inline formset...


@login_required
def add_bin(request, schedule_id):
    schedule_obj = get_object_or_404(Schedule, pk=schedule_id)

    if request.user != schedule_obj.author:
        raise PermissionDenied("You are not the author of this schedule.")

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.instance.schedule_id = schedule_obj
            if not form.instance.is_recurring:
                form.instance.recurring_type = None
                form.instance.separation_count = None
                form.instance.max_number_of_occurrences = None
            else:
                if form.instance.recurring_type is None or form.instance.separation_count is None or form.instance.max_number_of_occurrences is None:
                    form.add_error(
                        None, "Please provide values for recurring type, separation count, and max number of occurrences.")
                    events = Event.objects.filter(schedule_id=schedule_id)
                    return redirect(reverse('add_bin', kwargs={'schedule_id': schedule_id}))
            form.save()
            if 'add_another' in request.POST:
                return redirect(reverse('add_bin', kwargs={'schedule_id': schedule_id}))
            elif 'continue' in request.POST:
                return redirect(reverse('add_exception', kwargs={'schedule_id': schedule_id}))

    form = EventForm()
    events = Event.objects.filter(schedule_id=schedule_id)
    return render(request, 'schedulebuilder/event_form.html', {
        'form': form,
        'events': events,
    })


class AddException(CreateView, LoginRequiredMixin):
    form_class = ExceptionForm
    model = Exception
    success_url = reverse_lazy('create_schedule')

    def form_valid(self, form):
        # need to find a way to pass the event id into this view - i think i want to display an overview calendar before this view
        form.instance.event_id = Event.objects.last()
        return super().form_valid(form)


class CalendarView(TemplateView):
    template_name = 'schedulebuilder/calendar.html'