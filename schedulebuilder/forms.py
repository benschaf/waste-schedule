from .models import *
from wasteschedules.models import Schedule
from django import forms

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('title', 'description', 'locations')

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('kind', 'date', 'is_recurring', 'recurring_type', 'separation_count', 'max_number_of_occurrences')


class ExceptionForm(forms.ModelForm):
    class Meta:
        model = Exception
        fields = ('old_date', 'new_date', 'is_cancelled')
