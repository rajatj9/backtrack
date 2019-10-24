from django.db import models

# Create your models here.
class PBI(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    priority = models.IntegerField()
    status = models.CharField(max_length=50, default="Not Yet Started")
    estimate = models.IntegerField(default=0)

    def __str__(self):
        return self.name

