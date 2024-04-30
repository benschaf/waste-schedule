from django.db import models
from wasteschedules.models import Schedule

# Create your models here.
class Event(models.Model):

    variants = (
        (0, 'Restmüll'),
        (1, 'Biomüll'),
        (2, 'Papiermüll'),
        (4, 'Gelbe Tonne'),
    )

    patterns = (
        (0, 'not recurring'),
        (1, 'weekly'),
        (2, 'every other week'),
        (3, 'every third week'),
        (4, 'every fourth week'),
    )

    # I could / should use a separate is_recurring model - but for now I will keep it simple
    schedule_id = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='events')
    js_event_id = models.CharField(max_length=255)
    kind = models.IntegerField(choices=variants, default=0)
    date = models.DateField()
    # rrule fields - if rrule is not defined they are all null
    recurring_type = models.IntegerField(choices=patterns, default=0, null=True)
    separation_count = models.IntegerField(default=1, null=True)
    rrule_start = models.DateField(null=True)
    until = models.DateField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        # -> Credit for strftime: https://www.programiz.com/python-programming/datetime/strftime
        return self.date.strftime('%Y-%m-%d')


class Exception(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='exceptions')
    old_date = models.DateField()
    new_date = models.DateField(null=True, blank=True)
    is_cancelled = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["old_date"]

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')
