from django.urls import path
from . import views
from .api import views

urlpatterns = [
    path('pbi/', views.PBIListView.as_view(), name=None),
    path('pbi/create/', views.PBICreateView.as_view(), name=None),
    path('pbi/<int:pk>/', views.PBIDetailView.as_view(), name=None)
]