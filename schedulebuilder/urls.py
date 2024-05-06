from . import views
from django.urls import path

urlpatterns = [
    path('', views.PickLocation.as_view(), name='create_schedule'),
    path('title-description/<str:postal_code>', views.CreateSchedule.as_view(), name='create_schedule'),
    path('add-bins/<int:schedule_id>', views.EditCalendarView.as_view(), name='add_bins'),
    path('delete-schedule/<slug:slug>', views.DeleteSchedule.as_view(), name='delete_schedule'),
]