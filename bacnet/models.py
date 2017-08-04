from django.db import models
from energize_andover.models import School

class Data_Point(models.Model):
    Name = models.CharField(max_length=30)
    Time = models.CharField(max_length=30)
    Value = models.IntegerField(default=0)
    School = models.ForeignKey(School,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                               )

