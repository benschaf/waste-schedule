from django.urls import path
from . import views

urlpatterns = [
    path('', views.PickLocation.as_view(), name='pick_location'),
    path('title-description/<str:postal_code>',
         views.CreateSchedule.as_view(), name='create_schedule'),
    path('edit-schedule/<slug:slug>',
         views.UpdateSchedule.as_view(), name='edit_schedule'),
    path('add-bins/<int:schedule_id>',
         views.EditCalendarView.as_view(), name='add_bins'),
    path('delete-schedule/<slug:slug>',
         views.DeleteSchedule.as_view(), name='delete_schedule'),
]
