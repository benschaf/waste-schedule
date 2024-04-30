from . import views
from django.urls import path

urlpatterns = [
    path('', views.CreateSchedule.as_view(), name='create_schedule'),
    path('add-bins/<int:schedule_id>', views.EditCalendarView.as_view(), name='add_bins'),
    path('display-schedule/<int:schedule_id>', views.DisplayCalendarView.as_view(), name='display_schedule'),
    path('edit-schedule/<int:schedule_id>', views.EditScheduleView.as_view(), name='edit_schedule'),
]