from . import views
from django.urls import path

urlpatterns = [
    path('', views.ScheduleList.as_view(), name='schedule_list'),
    path('<slug:slug>/', views.ScheduleDetail.as_view(), name='schedule_detail'),
    path('schedule-like/<slug:slug>', views.ScheduleLike.as_view(), name='schedule_like'),
    path('schedule-subscribe/<slug:slug>', views.ScheduleSubscribe.as_view(), name='schedule_subscribe'),
]