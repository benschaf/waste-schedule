import json
from typing import Any
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import Event
from wasteschedules.models import Schedule, PostalCode
from .forms import PostalCodeForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.


class PickLocation(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    View for picking a location and creating a schedule for it.

    Inherits from LoginRequiredMixin, SuccessMessageMixin, and CreateView.
    """

    model = PostalCode
    form_class = PostalCodeForm
    template_name = 'schedulebuilder/location_form.html'
    success_message = "Location was created successfully."

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """
        Validates the form and creates a schedule for the selected location.
        If the location already exists, a message will be displayed on the next
        page.

        Args:
            form (BaseModelForm): The form containing the location details.

        Returns:
            HttpResponse: Opens the view to insert the schedule details if
                            the form is valid
        """
        postal_code = form.cleaned_data['postal_code']

        if PostalCode.objects.filter(postal_code=postal_code).exists():
            messages.add_message(self.request, messages.INFO,
                                    "Your Location already exists. Check out if there already is a schedule for it.")
            return HttpResponseRedirect(reverse('create_schedule', kwargs={'postal_code': postal_code}))

        return super().form_valid(form)

    def get_success_url(self) -> str:
        """
        Returns the URL to redirect to after the form is successfully submitted.

        Returns:
            str: The success URL redirects to the create_schedule view.
        """
        return reverse('create_schedule', kwargs={'postal_code': self.object.postal_code})


class CreateSchedule(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    View for creating a new schedule.

    Inherits from LoginRequiredMixin, SuccessMessageMixin, and CreateView.
    """

    login_url = reverse_lazy('account_login')
    redirect_field_name = None
    model = Schedule
    fields = ('title', 'description', 'image',)
    template_name = 'schedulebuilder/schedule_form.html'
    success_message = "Schedule was created successfully."

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Returns the context data for the view.

        Additional context data:
            - The postal code of the location.

        Returns:
            A dictionary containing the context data.
        """
        context = super().get_context_data(**kwargs)
        context['postcode'] = self.kwargs['postal_code']
        return context

    def form_valid(self, form):
        """
        Validates the form and sets the author of the schedule to the logged
        in user.

        Args:
            form: The form instance.

        Returns:
            The result of the parent class's form_valid method.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        Returns the URL to redirect to after a successful form submission.

        Adds the current schedule's location to the PostalCode model and redirects to the 'add_bins' view.

        Returns:
            The success URL.
        """
        self.object.locations.add(get_object_or_404(PostalCode, postal_code=self.kwargs['postal_code']))
        return reverse('add_bins', kwargs={'schedule_id': self.object.id})


class UpdateSchedule(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    A view for updating a schedule.

    Inherits from LoginRequiredMixin, SuccessMessageMixin, and UpdateView.
    """

    login_url = reverse_lazy('account_login')
    redirect_field_name = None
    model = Schedule
    fields = ('description', 'image',)
    template_name = 'schedulebuilder/update_schedule_form.html'
    success_message = "Schedule was updated successfully."

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Returns the context data for the view.

        Additional context data:
            - The postal code of the location.

        Returns:
            A dictionary containing the context data.
        """
        context = super().get_context_data(**kwargs)
        context['postcode'] = self.object.locations.all()[0]
        return context

    def get_success_url(self):
        """
        Returns the URL to redirect to after a successful update.

        Returns:
            The success URL redirects to the add_bins view.
        """
        return reverse('add_bins', kwargs={'schedule_id': self.object.id})

    def post(self, request, *args, **kwargs):
        """
        Handles the POST request.
        Checks if the user is the author of the schedule.

        Args:
            request: The HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The HTTP response.
        """
        if self.get_object().author != request.user:
            messages.add_message(self.request, messages.ERROR,
                                 "You are not the owner of this schedule.")
            return redirect(self.request.META.get('HTTP_REFERER', 'landing_page'))
        return super().post(request, *args, **kwargs)


class DeleteSchedule(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    A view for deleting a schedule.

    Inherits from LoginRequiredMixin, SuccessMessageMixin, and DeleteView.

    Methods:
        post(request, *args, **kwargs): Checks if the user is the owner of the schedule before deleting it.
        get_success_url(): Redirects to the schedule list page after the schedule is deleted.
    """
    login_url = reverse_lazy('account_login')
    redirect_field_name = None
    model = Schedule
    template_name = 'schedulebuilder/schedule_confirm_delete.html'
    success_message = "Schedule was deleted successfully."

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request for deleting the schedule.
        Checks if the user is the owner of the schedule before deleting it.

        If the user is not the owner of the schedule, an error message is added and the user is redirected
        to the previous page.

        Returns:
            HttpResponseRedirect: The redirect response.

        """
        if self.get_object().author != request.user:
            messages.add_message(self.request, messages.ERROR,
                                 "You are not the owner of this schedule.")
            return redirect(self.request.META.get('HTTP_REFERER', 'landing_page'))
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        """
        Returns the URL to redirect to after the schedule is deleted.

        The URL is generated based on the postal code of the first location associated with the schedule.

        Returns:
            str: The URL to redirect to the schedule list page.

        """
        return reverse('schedule_list', kwargs={'postcode': self.object.locations.all()[0].postal_code})

# maybe integrate this with the update or create events view - so the form can be displayed and post data using the same view
class EditCalendarView(LoginRequiredMixin, TemplateView):
    """
    View for editing a calendar.

    This view allows users to edit a calendar by updating the events associated with it.
    Only the owner of the calendar can access this view.

    Methods:
        dispatch(request, *args, **kwargs): Checks if the user is the owner of the schedule before rendering the view.
        get_context_data(schedule_id, **kwargs): Returns the context data for rendering the template.
        _convert_kind_to_int(kind): Helper method to convert the kind of event to an integer value.
        post(request, schedule_id): Writes the updated events from the post request to the database.
    """

    login_url = reverse_lazy('account_login')
    redirect_field_name = None
    template_name = 'schedulebuilder/calendar.html'

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handles the HTTP request and returns the HTTP response.
        Checks if the user is the owner of the schedule before rendering the view.

        Returns:
            HttpResponse: The HTTP response.

        Raises:
            Http404: If the schedule with the given ID does not exist.
        """
        schedule = get_object_or_404(Schedule, id=kwargs['schedule_id'])
        if schedule.author != request.user:
            messages.add_message(self.request, messages.ERROR,
                                 "You are not the owner of this schedule.")
            return redirect(self.request.META.get('HTTP_REFERER', 'landing_page'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, schedule_id, **kwargs):
        """
        Returns the context data for rendering the template.

        Additional context data:
            - The schedule object.
            - The postal code of the location.
            - The event data in JSON format.

        Args:
            schedule_id (int): The ID of the schedule.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        context["schedule"] = get_object_or_404(Schedule, id=schedule_id)
        context["postal_code"] = context["schedule"].locations.all()[0].postal_code

        events = Event.objects.filter(schedule_id=schedule_id)
        context["event_data"] = json.dumps(_event_to_json(events))

        return context

    def _convert_kind_to_int(self, kind):
        """
        Converts the kind of event to an integer value.

        Args:
            kind (str): The kind of event.

        Returns:
            int: The integer value corresponding to the kind of event.
        """
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
        """
        Handles the HTTP POST request and returns the HTTP response.
        Writes the updated events from the post request to the database.

        Args:
            request (HttpRequest): The HTTP request object.
            schedule_id (int): The ID of the schedule.

        Returns:
            JsonResponse: The JSON response.
            If the JSON data is valid, the response contains a redirect URL to
            the schedule detail page.

        Raises:
            Http404: If the schedule with the given ID does not exist.
        """
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

            messages.add_message(self.request, messages.SUCCESS,
                                 "Your Schedule events were saved successfully.")
            postcode = schedule.locations.all()[0]
            return JsonResponse({'redirect_url': reverse('schedule_detail', kwargs={'postcode': postcode, 'slug': schedule.slug})})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)


def _event_to_json(events):
    """
    Convert a list of FullCalendar events to a JSON representation.

    Args:
        events (list): A list of events.

    Returns:
        list: A list of dictionaries representing the events in JSON format.
    """
    event_list = []
    for event in events:
        event_list.append({
            'id': event.js_event_id,
            # -> Credit for get_kind_display(): https://docs.djangoproject.com/en/3.2/ref/models/instances/#django.db.models.Model.get_FOO_display
            'title': event.get_kind_display(),
            'start': event.date.isoformat(),
            'rrule': {
                'freq': event.recurring_type,
                'interval': event.separation_count,
                'dtstart': event.rrule_start.isoformat(),
                'until': event.until.isoformat(),
            } if event.recurring_type else None
        })
    return event_list
