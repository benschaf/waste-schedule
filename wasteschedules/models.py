from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

# Create your models here.


class Schedule(models.Model):
    """
    Represents a schedule for waste collection.

    Attributes:
        name (str): The name of the schedule.
        description (str): The description of the schedule.
        locations (ManyToManyField): The locations associated with the schedule.
        created_at (DateTimeField): The date and time when the schedule was created.
        updated_at (DateTimeField): The date and time when the schedule was last updated.
    """

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='schedules')
    description = models.TextField(blank=True)
    locations = models.ManyToManyField('Location', related_name='schedules')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title


def validate_postal_code(value):
    """
    Validates if a given value is a valid postal code.

    Args:
        value (str): The value to be validated.

    Raises:
        ValidationError: If the value is not a valid postal code.

    Returns:
        None
    """
    if len(value) != 5 or not value.isdigit():
        raise ValidationError(f'{value} is not a valid postal code')


class Location(models.Model):
    """
    Represents a location with a postal code and creation timestamp.

    Attributes:
        postal_code (str): The postal code of the location.
        created_at (datetime): The timestamp when the location was created.
    """

    postal_code = models.CharField(
        validators=[validate_postal_code], primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.postal_code


class Comment(models.Model):
    """
    Represents a comment made by a user on a schedule.
    """

    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule_id = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.commented_by}"


class Like(models.Model):
    """
    Represents a like given by a user to a schedule.
    """

    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule_id = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Like by {self.liked_by}"

class Subscription(models.Model):
    """
    Represents a subscription made by a user to a schedule.
    """

    subscribed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule_id = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    subscribed_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Subscription by {self.subscribed_by}"
