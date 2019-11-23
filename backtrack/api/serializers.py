from ..models import PBI, Sprint, Person, Project, Tasks
from rest_framework import serializers


class PBISerializer(serializers.ModelSerializer):
    class Meta:
        model = PBI
        fields = ('name', 'description', 'priority', 'story_points', 'status', 'id', 'project_id', 'sprint_id')  # if not declared, all fields of the model will be shown

class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ('id','start_date','end_date','capacity','project')

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('name', 'role', 'project', 'id')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name','id']

class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('id', 'pbi', 'description', 'name', 'developer', 'effort_hours','status')


