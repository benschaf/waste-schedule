from django.db import models
from wasteschedules.models import Schedule

# Create your models here.


class Event(models.Model):
    """
    Represents an event in the waste schedule.

    Attributes:
        schedule_id (ForeignKey): The foreign key to the Schedule model.
        js_event_id (CharField): The ID of the event in JavaScript.
        kind (IntegerField): The type of waste
            (0: Restmüll, 1: Biomüll, 2: Papiermüll, 4: Gelbe Tonne).
        date (DateField): The date of the event.
        recurring_type (IntegerField): The type of recurrence
            (0: not recurring, 1: weekly, 2: every other week,
            3: every third week, 4: every fourth week).
        separation_count (IntegerField):
            The number of separations for the event.
        rrule_start (DateField):
            The start date for the recurrence rule.
        until (DateField): The end date for the recurrence rule.
        created_on (DateTimeField):
            The date and time when the event was created.
    """

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

    schedule_id = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name='events')
    js_event_id = models.CharField(max_length=255)
    kind = models.IntegerField(choices=variants, default=0)
    date = models.DateField()
    recurring_type = models.IntegerField(
        choices=patterns, default=0, null=True)
    separation_count = models.IntegerField(default=1, null=True)
    rrule_start = models.DateField(null=True)
    until = models.DateField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
            Class that orders the query results based on the date field.
        """
        ordering = ["date"]

    def __str__(self):
        """
        Returns a string representation of the object.

        The returned string is formatted as a date in the format 'YYYY-MM-DD'.

        Returns:
            str: The string representation of the object.
        """
        return self.date.strftime('%Y-%m-%d')


class EventException(models.Model):
    """
    Represents an exception for an event in the waste schedule.

    Attributes:
        event_id (ForeignKey): The foreign key to the Event model.
        old_date (DateField): The original date of the event.
        new_date (DateField): The new date of the event (optional).
        is_cancelled (BooleanField): Indicates if the event is cancelled.
        created_on (DateTimeField):
            The date and time when the exception was created.

    Meta:
        ordering (list):
            The ordering of exceptions based on the old_date attribute.
    """

    event_id = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='exceptions')
    old_date = models.DateField()
    new_date = models.DateField(null=True, blank=True)
    is_cancelled = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Sorts the query results based on the old_date field.
        """
        ordering = ["old_date"]

    def __str__(self):
        """
        Returns a string representation of the object.

        The returned string is formatted as a date in the format 'YYYY-MM-DD'.

        Returns:
            str: The string representation of the object.
        """
        return self.old_date.strftime('%Y-%m-%d')
