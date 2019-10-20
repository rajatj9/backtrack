from django.urls import path
from . import views
from .api import views

urlpatterns = [
    path('', views.PBIListView.as_view(), name=None),
    path('create/', views.PBICreateView.as_view(), name=None),
    path('<int:pk>/', views.PBIDetailView.as_view(), name=None)
]