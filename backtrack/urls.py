from django.urls import path
from . import views
from .api import views

urlpatterns = [
    path('pbi/', views.PBIListAndCreateView.as_view(), name=None),
    path('pbi/<int:pk>/', views.PBIDetailView.as_view(), name=None)
]