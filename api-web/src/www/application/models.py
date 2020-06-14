from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.db.models import Max
from . import constants

class Command(models.Model):
    name = models.CharField(max_length=255, default='')
    namespace = models.CharField(max_length=255, default='')
    docker_image = models.TextField(default='')
    exec_command = models.TextField(default='')
    exec_args = models.TextField(default='')
    cpu_request = models.IntegerField(default=100)
    mem_request = models.IntegerField(default=100)
    cpu_limit = models.IntegerField(default=100)
    mem_limit = models.IntegerField(default=100)
    timeout = models.IntegerField(default=100)

class CommandVariable(models.Model):
    command = models.ForeignKey('Command')
    name = models.TextField(default='')
    value = models.TextField(default='')

class Crontab(models.Model):
    month = models.CharField(max_length=255, default='*')
    day = models.CharField(max_length=255, default='*')
    hour = models.CharField(max_length=255, default='*')
    minute = models.CharField(max_length=255, default='*')
    num_process = models.IntegerField(default=1)
    command = models.ForeignKey('Command')

class Process(models.Model):
    command = models.ForeignKey('Command')
    namespace = models.CharField(max_length=255, default='')
    timestamp = models.DateTimeField(default=timezone.now)
    pod_id = models.TextField(default='')
    pod_creation_log = models.TextField(default='')
    status = models.CharField(max_length=255, default='')
    message = models.TextField(default='')
    log = models.TextField(default='')
