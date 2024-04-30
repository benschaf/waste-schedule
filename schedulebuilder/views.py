import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from schedulebuilder.forms import *
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.


class CreateSchedule(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('account_login')
    redirect_field_name = None
    form_class = ScheduleForm
    template_name = 'schedulebuilder/schedule_form.html'
    model = Schedule

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('add_bins', kwargs={'schedule_id': self.object.id})

    # to add the location i will need an inline formset...


# maybe integrate this with the update or create events view - so the form can be displayed and post data using the same view
class CalendarView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('account_login')
    redirect_field_name = None
    template_name = 'schedulebuilder/calendar.html'

    def get_context_data(self, schedule_id, **kwargs):
        context = super().get_context_data(**kwargs)
        context["schedule"] = get_object_or_404(Schedule, id=schedule_id)
        return context

    def _convert_kind_to_int(self, kind):
        if kind == 'restmuell':
            return 0
        elif kind == 'biomuell':
            return 1
        elif kind == 'papiermuell':
            return 2
        elif kind == 'gelbe-tonne':
            return 4
        else:
            return None

    def post(self, request, schedule_id):
        schedule = get_object_or_404(Schedule, id=schedule_id)
        print(request.body)

        try:
            data = json.loads(request.body)
            # -> Credit for update_or_create: https://docs.djangoproject.com/en/5.0/ref/models/querysets/#update-or-create
            # -> Credit for dict.get(): https://www.w3schools.com/python/ref_dictionary_get.asp
            for event_data in data:
                kind = self._convert_kind_to_int(event_data['title'])
                print(event_data)
                event, created = Event.objects.update_or_create(
                    js_event_id=event_data['id'],
                    schedule_id = schedule,
                    defaults={
                        'kind': kind,
                        'date': event_data['start'],
                        'recurring_type': event_data.get('rrule', {}).get('freq', None),
                        'separation_count': event_data.get('rrule', {}).get('interval', None),
                        'rrule_start': event_data.get('rrule', {}).get('dstart', None),
                        'until': event_data.get('rrule', {}).get('until', None),
                    }
                )
            # oh and also i need to find out how to add exceptions to the rrule data
            return JsonResponse({'message': 'Success'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)