from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.urls import reverse
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

# Create your models here.


class Schedule(models.Model):
    """
    Represents a schedule for waste collection.

    Attributes:
        name (str): The name of the schedule.
        description (str): The description of the schedule.
        locations (ManyToManyField): The locations associated with the
            schedule.
        created_at (DateTimeField): The date and time when the schedule was
            created.
        updated_at (DateTimeField): The date and time when the schedule was
            last updated.
    """

    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='schedules')
    description = models.TextField()
    locations = models.ManyToManyField('PostalCode', related_name='schedules')
    image = CloudinaryField(
        'image', null=True, blank=True, default='placeholder')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Orders the query results based on the created_on field.
        """
        ordering = ["-created_on"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns the title of the schedule a string representation of the
        object.

        Returns:
            str: A string representation of the object.
        """
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


class PostalCode(models.Model):
    """
    Represents a postal code.

    Attributes:
        postal_code (str): The postal code value.
    """

    postal_code = models.CharField(
        validators=[validate_postal_code], max_length=5, unique=True)

    def __str__(self):
        return self.postal_code


class Comment(models.Model):
    """
    Represents a comment made by a user on a schedule.
    """

    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule_id = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    body = models.TextField()
    edited = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.commented_by}"

    def get_absolute_url(self):
        """
        Returns the absolute URL for the schedule detail view of the
        WasteSchedule object.

        The URL is generated using the reverse function and the schedule's
        attributes.

        Returns:
            str: The absolute URL for the schedule detail view.
        """
        return reverse('schedule_detail', kwargs={
            'postcode': self.schedule_id.locations.all()[0],
            'slug': self.schedule_id.slug})


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
