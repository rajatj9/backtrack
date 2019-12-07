from datetime import *

from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import *


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
        if (all_tasks_completed and len(tasks) > 0):
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
        if (all_tasks_completed and len(tasks) > 0):
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
    #     #             developer = Developer.objects.get(pk=developer_id)
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

    def check_date_pass(self, end_date):
        if(datetime.today().date() > end_date):
            return True
        else:
            return False

    def retrieve(self, request, *args, **kwargs):
        super().retrieve(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        self.check_completion(data['id'])
        for p in Sprint.objects.all():
            if (self.check_date_pass(p.end_date)):  # check if the date for any sprint has passed
                p.status = "COMPLETED"

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
        try:
            current_sprint = sprints.latest()
            serializer = SprintSerializer(current_sprint)
            data = serializer.data

            # get PBI objects for this sprint from its sprint id
            pbis = PBI.objects.filter(sprint_id=current_sprint.id)
            data["pbis"] = []
            for pbi in pbis:
                pbi_serialized = PBISerializer(pbi)
                # get the tasks for this PBI
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
        except:
            response = {"status_code": status.HTTP_404_NOT_FOUND,
                        "message": "No current Sprint!"}
            return Response(response)

class DeveloperCreateAndListView(generics.ListCreateAPIView):
    queryset = Developer.objects.filter(project=None)
    serializer_class = DeveloperSerializer

    def create(self, request, *args, **kwargs):
        super(DeveloperCreateAndListView, self).create(request, args, kwargs)
        response = {"status_code": status.HTTP_201_CREATED,
                    "message": "Successfully created",
                    "result": request.data}
        return Response(response)


class DeveloperListView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer


class PBIInProjectView(generics.ListAPIView):
    queryset = PBI.objects.all()
    serializer_class = PBISerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        needed_project = request.GET['id']
        pbis = PBI.objects.filter(project_id=needed_project)
        returned_pbi_ids = []
        for pbi in pbis:
            returnable = {}
            returnable['id'] = pbi.id
            returnable['name'] = pbi.name
            returnable['description'] = pbi.description
            returnable['priority'] = pbi.priority
            returnable['story_points'] = pbi.story_points
            if (pbi.sprint_id != None):
                returnable['sprint_id'] = pbi.sprint_id.id
            else:
                returnable['sprint_id'] = pbi.sprint_id
            returnable['status'] = pbi.status
            returned_pbi_ids.append(returnable)
        print(returned_pbi_ids)
        returnable = sorted(returned_pbi_ids, key=lambda k: k['priority'], reverse=False)
        response = {"status_code": status.HTTP_200_OK, "message": "Retreived!", "result": returnable}
        return Response(response)


class ManagerProjectsView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        needed_manager = request.GET['id']
        projects = Project.objects.filter(manager=needed_manager)
        returned_project_ids = []
        for project in projects:
            returnable = {}
            returnable['project_id'] = project.id
            returnable['project_name'] = project.name
            returned_project_ids.append(returnable)  # also project name
        print(returned_project_ids)
        response = {"status_code": status.HTTP_200_OK, "message": "Retreived!", "result": returned_project_ids}
        return Response(response)


class ProjectCreateAndListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    def create(self, request, *args, **kwargs):
        request.GET._mutable = True
        developers = request.data.pop('developers')
        owner = Developer.objects.filter(id=request.data['owner'])
        if (owner[0].project != None):
            response = {"status_code": status.HTTP_406_NOT_ACCEPTABLE,
                        "message": "Product owner can't create more than one project"}
            return Response(response)
        else:
            super(ProjectCreateAndListView, self).create(request, args, kwargs)
            project_id = Project.objects.get(name=request.data['name']).id
            owner.update(project=project_id)
            owner.update(role="Product Owner")
            recipient_list = []
            manager = Manager.objects.get(id=request.data['manager'])
            for dev_id in developers:
                dev = Developer.objects.filter(id=dev_id)
                dev.update(project=project_id)
                user = User.objects.get(username=dev[0].user)
                recipient_list.append(user.email)
            subject = "You have been added to project " + request.data['name'] + "!"
            message = " You were added to the new project " + request.data['name'] + " by " + manager.name
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, recipient_list)
            response = {"status_code": status.HTTP_201_CREATED,
                        "message": "Successfully created",
                        "result": request.data,
                        "project_id": project_id}
            return Response(response)


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


class ManagersCreateAndListView(generics.ListCreateAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    def create(self, request, *args, **kwargs):
        super(ManagersCreateAndListView, self).create(request, args, kwargs)
        response = {"status_code": status.HTTP_201_CREATED,
                    "message": "Successfully created",
                    "result": request.data}
        return Response(response)


# users API to view user details
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer