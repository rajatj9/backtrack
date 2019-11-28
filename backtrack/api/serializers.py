from ..models import PBI, Sprint, Developer, Project, Tasks, Manager,User
from rest_framework import serializers
from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.authtoken.models import Token



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
        fields = ('id','user','name','project', 'role')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id','name','manager')

class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('id', 'pbi', 'description', 'name', 'developer', 'effort_hours','status')

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ('id','user','name')


#Users model serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email', 'username', 'password', 'is_developer', 'is_manager')


class CustomRegisterSerializer(RegisterSerializer):
    is_developer = serializers.BooleanField()
    is_manager = serializers.BooleanField()

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'is_developer', 'is_manager')

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'is_developer': self.validated_data.get('is_developer', ''),
            'is_manager': self.validated_data.get('is_manager', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.is_developer = self.cleaned_data.get('is_developer')
        user.is_manager = self.cleaned_data.get('is_manager')
        user.save()
        adapter.save_user(request, user, self)
        return user

class CustomTokenSerializer(serializers.ModelSerializer):

    user_info = serializers.SerializerMethodField()

    class Meta:
        model = Token
        fields = ('key','user','user_info')

    #token serializer for getting the project id of developer
    def get_user_info(self,obj):
        serializer_data = UserSerializer(obj.user).data
        print(serializer_data)
        is_developer = serializer_data.get('is_developer')
        is_manager = serializer_data.get('is_manager')
        project_id = -1
        if is_developer == True:
            try:
                developer_obj = Developer.objects.get(user=obj.user)
                project_id = developer_obj.project.id
            except Developer.DoesNotExist:
                print("No developer connected with this user yet")
        return {
            'is_developer': is_developer,
            'is_manager': is_manager,
            'project_id': project_id
        }
