from ..models import PBI, Sprint, Project, Person, Tasks
from .serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from datetime import *

class PBICreateAndListView(generics.ListCreateAPIView):

    queryset = PBI.objects.all().order_by('priority')
    serializer_class = PBISerializer

    def get(self, request, *args, **kwargs):
        for q in PBI.objects.all():
            self.check_completion(q.id)
        return self.list(request, *args, **kwargs)

    def check_completion(self, pbi_id):
        tasks = Tasks.objects.filter(pbi= pbi_id)
        print("TASKS:", tasks)
        all_tasks_completed = True
        for task in tasks:
            if(task.status!="COMPLETED"):
                all_tasks_completed = False
                break
        if(all_tasks_completed):
            PBI.objects.filter(id=pbi_id).update(status="COMPLETED")

    def update_priorities(self, inserting_priority):
        lower_priorities = PBI.objects.filter(priority__gte=inserting_priority)
        for item in lower_priorities:
            item.priority += 1
            item.save()

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

    def check_completion(self, pbi_id):
        tasks = Tasks.objects.filter(pbi= pbi_id)
        print("TASKS:", tasks)
        all_tasks_completed = True
        for task in tasks:
            if(task.status!="COMPLETED"):
                all_tasks_completed = False
                break
        if(all_tasks_completed):
            PBI.objects.filter(id=pbi_id).update(status="COMPLETED")

    def update_priorities(self, inserting_priority):
        lower_priorities = PBI.objects.filter(priority__gt=inserting_priority)
        for item in lower_priorities:
            item.priority -= 1
            item.save()

    def retrieve(self, request, *args, **kwargs):
        super(PBIDetailView, self).retrieve(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        id_to_send = data['id']
        self.check_completion(id_to_send)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully retrieved",
                    "result": data}
        return Response(response)

    def patch(self, request, *args, **kwargs):
        super(PBIDetailView, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        if 'sprint_id' in request.data and 'status' in request.data:
            Tasks.objects.filter(pbi=data['id']).delete()
            Tasks.objects.filter(pbi=data['id']).delete()
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully updated",
                    "result": data}
        return Response(response)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        priority = data['priority']
        super(PBIDetailView, self).delete(request, args, kwargs)
        self.update_priorities(priority)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully deleted"}
        return Response(response)

class SprintCreateAndListView(generics.ListCreateAPIView):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer

    def check_pbi_completion(self, sprint_id):
        pbis = PBI.objects.filter(sprint_id = sprint_id)
        all_pbis_completed = True
        for pbi in pbis:
            if(pbi.status!="COMPLETED"):
                all_pbis_completed = False
                break
        if(all_pbis_completed):
            Sprint.objects.filter(id=sprint_id).update(status="COMPLETED")

    def check_date_pass(self, end_date):
        if(datetime.today().date() > end_date):
            return True
        else:
            return False

    def get(self, request, *args, **kwargs):
        for p in Sprint.objects.all():
            self.check_pbi_completion(p.id) #check if PBI is completed
            if(self.check_date_pass(p.end_date)): #check if the date has passed
                p.status = "COMPLETED"

        return self.list(request, *args, **kwargs)
    #
    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    #     project_id = request.data['project']
    #     project = Project.objects.get(pk=project_id)
    #     Sprint.objects.create(**request.data, project=project)
    #     # for pbi in pbis:
    #     #     pbi_id = pbi["pbi_id"]
    #     #     pbi_obj = PBI.objects.get(pk=pbi_id)
    #     #     PBI.objects.filter(pk=pbi_id).update(sprint_id=sprint)
    #     #     PBI.objects.filter(pk=pbi_id).update(state="ONGOING")
    #     #     for task in pbi["tasks"]:
    #     #         if 'developer' in task:
    #     #             developer_id = task.pop('developer')
    #     #             developer = Person.objects.get(pk=developer_id)
    #     #             print(developer)
    #     #             Tasks.objects.create(pbi=pbi_obj, developer=developer, **task)
    #     #         else:
    #     #             Tasks.objects.create(pbi=pbi_obj, **task)
    #     response = {"status_code": status.HTTP_201_CREATED,
    #                 "message": "Successfully created",
    #                 "result": request.data}
    #     return Response(response)

class SprintListView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer

    def check_completion(self, sprint_id):
        pbis = PBI.objects.filter(sprint_id = sprint_id)
        all_pbis_completed = True
        for pbi in pbis:
            if(pbi.status!="COMPLETED"):
                all_pbis_completed = False
                break
        if(all_pbis_completed):
            Sprint.objects.filter(id=sprint_id).update(status="COMPLETED")

    def retrieve(self, request, *args, **kwargs):
        super().retrieve(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        self.check_completion(data['id'])
        pbis = PBI.objects.filter(sprint_id=instance.id)
        data["pbis"] = []
        for pbi in pbis:
            pbi_serialized = PBISerializer(pbi)
            task_for_pbi = Tasks.objects.filter(pbi=pbi.id)
            task_serialized = TasksSerializer(task_for_pbi,many=True)
            temp = {}
            temp["pbi_id"] = pbi.id
            temp["name"] = pbi.name
            temp["tasks"] = task_serialized.data
            temp["status"] = pbi.status
            data["pbis"].append(temp)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully retrieved",
                    "result": data}
        return Response(response)

class CurrentSprintView(generics.RetrieveUpdateDestroyAPIView):
    #we first get the project object first from the project ID
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def retrieve(self,request,*args,**kwargs):
        super().retrieve(request, args, kwargs)
        project_instance = self.get_object()
        # get this sprint objects belonging to this project
        sprints = Sprint.objects.filter(project=project_instance)

        #get the most recent sprint (by start_date)
        current_sprint = sprints.latest()
        serializer = SprintSerializer(current_sprint)
        data = serializer.data

        #get PBI objects for this sprint from its sprint id
        pbis = PBI.objects.filter(sprint_id=current_sprint.id)
        data["pbis"] = []
        for pbi in pbis:
            pbi_serialized = PBISerializer(pbi)
            #get the tasks for this PBI
            task_for_pbi = Tasks.objects.filter(pbi=pbi.id)
            task_serialized = TasksSerializer(task_for_pbi, many=True)
            temp = {}
            temp["pbi_id"] = pbi.id
            temp["name"] = pbi.name
            temp["tasks"] = task_serialized.data
            data["pbis"].append(temp)

        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully retrieved",
                    "result": data}
        return Response(response)

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

    def create(self, request, *args, **kwargs):
        request.GET._mutable = True
        sprint_id = request.data.pop('sprint_id')
        pbi_id = request.data['pbi_id']
        pbi = PBI.objects.filter(pk=pbi_id)
        pbi.update(sprint_id=sprint_id)
        pbi.update(status="ONGOING")
        Tasks.objects.create(**request.data)
        response = {"status_code": status.HTTP_201_CREATED,
                    "message": "Successfully created",
                    "result": request.data}
        return Response(response)

class TasksListView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        super(TasksListView, self).delete(request, args, kwargs)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully deleted",
                    "result": data}
        return Response(response)

    def patch(self, request, *args, **kwargs):
        super(TasksListView, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully updated",
                    "result": data}
        return Response(response)
