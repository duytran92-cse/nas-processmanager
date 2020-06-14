from django.core import serializers
from django.db.models import Q
from notasquare.urad_api import *
from application.models import *
from application import constants

from application.modules.common import helpers

class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = Process.objects
        if 'text' in data:
            pass
        return query
    def serialize_entry(self, process):
        return {
            'id':                 process.id,
            'timestamp':          process.timestamp,
            'command_id':         process.command_id,
            'command_label':      process.command.name,
            'pod_id':             process.pod_id,
            'status':             process.status,
            'message':            process.message
        }


class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        process = Process.objects.get(pk=data['id'])
        api = helpers.KubernetesAPI()

        result = {
            'id':                 process.id,
            'timestamp':          process.timestamp,
            'command_id':         process.command_id,
            'command_label':      process.command.name,
            'pod_id':             process.pod_id,
            'status':             process.status,
            'message':            process.message,
            'log':                process.log,
        }
        return result

class Log_Process(handlers.standard.GetHandler):
    def get_data(self, data):
        process = Process.objects.get(pk=data['id'])
        #print process.__dict__
        return serializers.serialize("json", [process,])

class Stop_Process(handlers.standard.GetHandler):
    def get_data(self, data):
        process = Process.objects.get(pk=data['id'])
        process.status = 'Stop'
        process.save()
        #print process.__dict__
        return serializers.serialize("json", [process,])

class Clean_Process(handlers.standard.GetHandler):
    def get_data(self, data):
        process = Process.objects.filter(~Q(status__in=['Running'])).all()
        i = 0
        #print len(process)
        for p in process:
            p.delete()
            i += 1
        return {'process_delete': i}

