from django.urls import path
from . import views
from .api import views

urlpatterns = [
    path('pbi/', views.PBICreateAndListView.as_view(), name=None),
    path('pbi/<int:pk>/', views.PBIDetailView.as_view(), name=None),
    path('tasks/', views.TasksCreateAndListView.as_view(), name=None),
    path('tasks/<int:pk>/', views.TasksListView.as_view(), name=None),
    path('developers/', views.DeveloperCreateAndListView.as_view(), name=None),
    path('developer/<int:pk>/', views.DeveloperListView.as_view(), name=None),
    path('project/', views.ProjectCreateAndListView.as_view(), name=None),
    path('project/<int:pk>/', views.ProjectListView.as_view(), name=None),
    path('sprint/', views.SprintCreateAndListView.as_view(), name=None),
    path('sprint/<int:pk>/', views.SprintListView.as_view(), name=None), #pk is sprint_id
    path('currentsprint/<int:pk>/',views.CurrentSprintView.as_view(),name=None), #pk is project_id
    path('managers/', views.ManagersCreateAndListView.as_view(), name=None)
]

#/project: Project name and manager ID, list of developer IDs I have to traverse and add that that project name to them