from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=200)

class Person(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Sprint(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

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
    developer = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    pbi = models.ForeignKey(PBI, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    effort_hours = models.IntegerField()

    def __str__(self):
        return self.name

