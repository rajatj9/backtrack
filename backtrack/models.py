from django.db import models

# Create your models here.
class PBI(models.Model):
    name = models.CharField(max_length=250,default="")
    description = models.TextField(default="")
    priority = models.IntegerField(default=0)
    estimate = models.IntegerField(default=0)
    status = models.CharField(max_length=50,default="Not Yet Started")


    def __str__(self):
        return self.name
