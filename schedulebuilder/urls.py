from . import views
from django.urls import path

urlpatterns = [
    path('', views.CreateSchedule.as_view(), name='create_schedule'),
    path('add-bin/<int:schedule_id>', views.add_bin, name='add_bin'),
    path('add-exceptions/<int:schedule_id>', views.AddException.as_view(), name='add_exception'),
    path('calendar', views.CalendarView.as_view(), name='calendar'),
]