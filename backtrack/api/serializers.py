from ..models import PBI, Sprint, Developer, Project, Tasks, Manager
from rest_framework import serializers


class PBISerializer(serializers.ModelSerializer):
    class Meta:
        model = PBI
        fields = ('name', 'description', 'priority', 'story_points', 'status', 'id', 'project_id', 'sprint_id')  # if not declared, all fields of the model will be shown

class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ('id','start_date','end_date','capacity','project', 'status')

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ('id', 'name', 'project', 'role')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name','manager')

class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('id', 'pbi', 'description', 'name', 'developer', 'effort_hours','status')

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ('id', 'name')

