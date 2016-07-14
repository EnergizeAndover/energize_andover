from django.db import models
from energize_andover.script.file_transfer import _temporary_output_file_path
import pandas as pd
# Create your models here.
class SmartGraph(models.Model):

    graph_data = models.CharField(max_length=100,
                                  choices=[(choice, choice)for choice in pd.read_csv(_temporary_output_file_path(),
                                                                                     header=1, index_col=[0]).columns],
    )

    def __init__(self, *args, **kwargs):
        super(SmartGraph, self).__init__(*args, **kwargs)
        self.fields['graph_data'].choices = [(choice, choice)for choice in pd.read_csv(_temporary_output_file_path(), header=1, index_col=[0]).columns]


