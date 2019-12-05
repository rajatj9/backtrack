from django.contrib.auth.models import AbstractUser
from django.db import models


#This model is made for an abstract Account model (passwords,email,username)
class User(AbstractUser):
    is_developer = models.BooleanField()
    is_manager = models.BooleanField()
    def __str__(self):
        return self.username

class Manager(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE) #Manager has one to one relation with User
    name = models.CharField(max_length=200)

class Project(models.Model):
    name = models.CharField(max_length=200)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    owner = models.CharField(max_length=200, default="Not Yet Assigned")

class Developer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, default="developer")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

class Sprint(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="Ongoing")
    #this is for getting the most recent sprint by start date
    class Meta:
        get_latest_by = 'start_date'

# Create your models here.
class PBI(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    priority = models.IntegerField()
    status = models.CharField(max_length=50, default="Not Yet Started")
    story_points = models.IntegerField(default=0)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    sprint_id = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True)

class Tasks(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, null=True)
    pbi = models.ForeignKey(PBI, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    effort_hours = models.IntegerField()
    status = models.CharField(max_length=100, default="Not Yet Started")

    def __str__(self):
        return self.name