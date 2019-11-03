
from ..models import PBI, Sprint, Project, Person, Tasks
from .serializers import *
from rest_framework import generics, status
from rest_framework.response import Response

class PBICreateAndListView(generics.ListCreateAPIView):
    queryset = PBI.objects.all().order_by('priority')
    serializer_class = PBISerializer

    def update_priorities(self, inserting_priority):
        lower_priorities = PBI.objects.filter(priority__gte=inserting_priority)
        for item in lower_priorities:
            item.priority += 1
        lower_priorities.update()

    def create(self, request, *args, **kwargs):
        inserting_priority = request.data['priority']
        self.update_priorities(inserting_priority)
        super(PBICreateAndListView, self).create(request, args, kwargs)
        response = {"status_code": status.HTTP_201_CREATED,
                    "message": "Successfully created",
                    "result": request.data}
        return Response(response)

class PBIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PBI.objects.all()
    serializer_class = PBISerializer

    def retrieve(self, request, *args, **kwargs):
        super(PBIDetailView, self).retrieve(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully retrieved",
                    "result": data}
        return Response(response)

    def patch(self, request, *args, **kwargs):
        super(PBIDetailView, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully updated",
                    "result": data}
        return Response(response)

    def delete(self, request, *args, **kwargs):
        super(PBIDetailView, self).delete(request, args, kwargs)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully deleted"}
        return Response(response)

class SprintCreateAndListView(generics.ListCreateAPIView):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        pbis = request.data.pop('pbis')
        project_id = request.data.pop('project')
        project = Project.objects.get(pk=project_id)
        sprint = Sprint.objects.create(**request.data, project=project)
        for pbi in pbis:
            pbi_id = pbi["pbi_id"]
            pbi_obj = PBI.objects.get(pk=pbi_id)
            PBI.objects.filter(pk=pbi_id).update(sprint_id=sprint)
            for task in pbi["tasks"]:
                if 'developer' in task:
                    developer_id = task.pop('developer')
                    developer = Person.objects.get(pk=developer_id)
                    print(developer)
                    Tasks.objects.create(pbi=pbi_obj, developer=developer, **task)
                else:
                    Tasks.objects.create(pbi=pbi_obj, **task)
        response = {"status_code": status.HTTP_201_CREATED,
                    "message": "Successfully created",
                    "result": request.data}
        return Response(response)

class SprintListView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SprintSerializer
    queryset = Sprint.objects.all()

class PersonCreateAndListView(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class PersonListView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class ProjectCreateAndListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectListView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class TasksCreateAndListView(generics.ListCreateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer

class TasksListView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
