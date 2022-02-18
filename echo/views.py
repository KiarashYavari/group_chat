from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class IndexView(TemplateView):
    template_name = "echo/index.html"

class ImageEchoView(TemplateView):
    template_name = "echo/image_echo.html"