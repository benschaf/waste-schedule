from django.contrib import admin
from .models import Event, EventException

# Register your models here.
admin.site.register(Event)
admin.site.register(EventException)
