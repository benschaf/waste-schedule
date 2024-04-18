from django.contrib import admin
from .models import Schedule, Location, Comment, Like, Subscription

# Register your models here.
admin.site.register(Schedule)
admin.site.register(Location)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Subscription)
