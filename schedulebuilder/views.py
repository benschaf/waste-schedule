import json
from django.http import HttpRequest, HttpResponseForbidden, JsonResponse
from django.http.response import HttpResponse
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
class EditCalendarView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('account_login')
    redirect_field_name = None
    template_name = 'schedulebuilder/calendar.html'

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        schedule = get_object_or_404(Schedule, id=kwargs['schedule_id'])
        if schedule.author != request.user:
                return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, schedule_id, **kwargs):
        context = super().get_context_data(**kwargs)
        context["schedule"] = get_object_or_404(Schedule, id=schedule_id)

        events = Event.objects.filter(schedule_id=schedule_id)
        context["event_data"] = json.dumps(_event_to_json(events))

        return context

    def _convert_kind_to_int(self, kind):
        if kind == 'Restmüll':
            return 0
        elif kind == 'Biomüll':
            return 1
        elif kind == 'Papiermüll':
            return 2
        elif kind == 'Gelbe Tonne':
            return 4
        else:
            return None

    def post(self, request, schedule_id):
        schedule = get_object_or_404(Schedule, id=schedule_id)
        try:
            data = json.loads(request.body)
            # -> Credit for update_or_create: https://docs.djangoproject.com/en/5.0/ref/models/querysets/#update-or-create
            # -> Credit for dict.get(): https://www.w3schools.com/python/ref_dictionary_get.asp
            for event_data in data:
                kind = self._convert_kind_to_int(event_data['title'])
                event, created = Event.objects.update_or_create(
                    js_event_id=event_data['id'],
                    schedule_id=schedule,
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
            postcode = schedule.locations.all()[0]
            return JsonResponse({'redirect_url': reverse('schedule_detail', kwargs={'postcode': postcode, 'slug' : schedule.slug})})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)


def _event_to_json(events):
    event_list = []
    for event in events:
        event_list.append({
            'id': event.js_event_id,
            # -> Credit for get_kind_display(): https://docs.djangoproject.com/en/3.2/ref/models/instances/#django.db.models.Model.get_FOO_display
            'title': event.get_kind_display(),
            'start': event.date.isoformat(),
            'rrule': {
                'freq': event.recurring_type,
                'dtstart': event.rrule_start.isoformat(),
                'until': event.until.isoformat(),
            } if event.recurring_type else None
        })
    return event_list
