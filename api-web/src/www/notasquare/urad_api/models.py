import json, datetime
from django.db import models
from django.utils import timezone
from . import constants

# RBAC Authorizator
class User(models.Model):
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255, default='')
    is_disabled = models.BooleanField(default=False)

class Group(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, default='')
    is_disabled = models.BooleanField(default=False)

# Queue
class Job(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    kind = models.CharField(max_length=255)
    parameters = models.TextField(default='')
    result = models.TextField(default='')
    status = models.CharField(max_length=50, choices=constants.JOB_STATUS, default='open')
    last_updated = models.DateTimeField(default=timezone.now)
    last_message = models.TextField(default='')

class JobMessage(models.Model):
    job = models.ForeignKey('Job')
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()
