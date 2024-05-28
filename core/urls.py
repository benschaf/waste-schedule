from . import views
from django.urls import path

urlpatterns = [
    path('', views.LandingPage.as_view(), name='landing_page'),
    path('about/', views.AboutPage.as_view(), name='about_page'),
]