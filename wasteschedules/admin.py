from django.contrib import admin
from .models import Schedule, PostalCode, Comment, Like, Subscription

# Register your models here.
admin.site.register(Schedule)
admin.site.register(PostalCode)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Subscription)
