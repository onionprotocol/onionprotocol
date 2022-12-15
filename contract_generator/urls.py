from django.urls import path
from . import views

app_name = "contract_generator"

urlpatterns = [
    path("", views.IndexView, name="index"),
    path("generator/", views.GeneratorView, name="generator"),
    
]