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

# Create your models here.
class PBI(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    priority = models.IntegerField()
    status = models.CharField(max_length=50, default="Not Yet Started")
    story_points = models.IntegerField(default=0)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    sprint_id = models.ForeignKey(Sprint, on_delete=models.CASCADE, default="NULL")

class Tasks(models.Model):
    sprint_id = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    pbi_id = models.ForeignKey(PBI, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    effort_hours = models.IntegerField()

    def __str__(self):
        return self.name

