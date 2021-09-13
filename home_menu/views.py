from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = "about.html"


def home(request):
    return render(request, 'home_menu/home.html')
