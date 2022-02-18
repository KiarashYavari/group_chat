from django.urls import path
from .views import IndexView, ImageEchoView

urlpatterns = [
    path('', IndexView.as_view(), name="echo_index"),
    path('image/', ImageEchoView.as_view(), name="echo_image"),    
]