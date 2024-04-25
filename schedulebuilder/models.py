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
        (0, 'weekly'),
        (2, 'monthly'),
    )

    # I could / should use a separate is_recurring model - but for now I will keep it simple
    schedule_id = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='events')
    kind = models.IntegerField(choices=variants, default=0)
    date = models.DateField()
    is_recurring = models.BooleanField(default=False)
    recurring_type = models.IntegerField(choices=patterns, default=0, null=True, blank=True)
    separation_count = models.IntegerField(default=1, null=True, blank=True)
    max_number_of_occurrences = models.IntegerField(default=12, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return self.date


class Exception(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='exceptions')
    old_date = models.DateField()
    new_date = models.DateField(null=True, blank=True)
    is_cancelled = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["old_date"]

    def __str__(self):
        return self.date
