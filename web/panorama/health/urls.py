# Packages
from django.urls import re_path

# Project
from . import views

urlpatterns = [
    re_path(r"^health$", views.health),
]
