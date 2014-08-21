from django.db import models


class Task(models.Model):
    text = models.CharField(max_length=255)
    filepath = models.CharField(max_length=255)
    line_number = models.IntegerField(null=True, default=None)
    closed = models.BooleanField(default=False)
    creation_time = models.DateTimeField(auto_now_add=True)
    # assigned = None
    # commit = None
    # repository = None
