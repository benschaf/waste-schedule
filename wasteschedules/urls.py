from . import views
from django.urls import path

urlpatterns = [
    path('', views.ScheduleList.as_view(), name='schedule_list'),
    path('<slug:slug>/', views.ScheduleDetail.as_view(), name='schedule_detail'),
]