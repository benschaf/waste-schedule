from . import views
from django.urls import path

urlpatterns = [
    path('', views.ScheduleList.as_view(), name='schedule_list'),
    path('<slug:slug>/', views.ScheduleDetail.as_view(), name='schedule_detail'),
    path('schedule-like/<slug:slug>', views.ScheduleLike.as_view(), name='schedule_like'),
    path('schedule-subscribe/<slug:slug>', views.ScheduleSubscribe.as_view(), name='schedule_subscribe'),
    path('schedule-comment/<slug:slug>', views.ScheduleComment.as_view(), name='schedule_comment'),
    path('schedule-comment-update/<int:pk>/<slug:slug>', views.schedule_comment_edit, name='schedule_comment_update'),
    path('schedule-comment-delete/<int:pk>', views.ScheduleCommentDelete.as_view(), name='schedule_comment_delete'),
]