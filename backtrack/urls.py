from django.urls import path
from . import views
from .api import views

urlpatterns = [
    path('', views.PBIListView.as_view(), name=None)
]