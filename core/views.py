from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class LandingPage(TemplateView):
    """
    A view that renders the landing page of the website.
    """
    template_name = 'core/index.html'

class AboutPage(TemplateView):
    """
    A view that renders the about page of the website.
    """
    template_name = 'core/about.html'