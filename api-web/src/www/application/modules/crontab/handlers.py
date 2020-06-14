from notasquare.urad_api import *
from application.models import *
from application import constants


class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = Crontab.objects
        if 'text' in data:
            pass
        return query
    def serialize_entry(self, crontab):
        return {
            'id':                 crontab.id,
            'month':              crontab.month,
            'day':                crontab.day,
            'hour':               crontab.hour,
            'minute':             crontab.minute,
            'command_id':         crontab.command_id,
            'command_label':      crontab.command.name,
            'num_process':        crontab.num_process
        }


class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        crontab = Crontab.objects.get(pk=data['id'])

        result = {
            'id':                 crontab.id,
            'month':              crontab.month,
            'day':                crontab.day,
            'hour':               crontab.hour,
            'minute':             crontab.minute,
            'command_id':         crontab.command_id,
            'command_label':      crontab.command.name,
            'num_process':        crontab.num_process
        }
        return result


class Create(handlers.standard.CreateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('month', 'string'):
            self.add_error('month', 'MUST_NOT_BE_EMPTY')
        if not parser.parse('day', 'string'):
            self.add_error('day', 'MUST_NOT_BE_EMPTY')
        if not parser.parse('hour', 'string'):
            self.add_error('hour', 'MUST_NOT_BE_EMPTY')
        if not parser.parse('minute', 'string'):
            self.add_error('minute', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def create(self, data):
        crontab = Crontab()
        crontab.month = data['month']
        crontab.day = data['day']
        crontab.hour = data['hour']
        crontab.minute = data['minute']
        crontab.command_id = data['command_id']
        crontab.num_process = data['num_process']
        crontab.save()
        return crontab


class Update(handlers.standard.UpdateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if 'month' in params:
            if not parser.parse('month', 'string'):
                self.add_error('month', 'MUST_NOT_BE_EMPTY')
        if 'day' in params:
            if not parser.parse('day', 'string'):
                self.add_error('day', 'MUST_NOT_BE_EMPTY')
        if 'hour' in params:
            if not parser.parse('hour', 'string'):
                self.add_error('hour', 'MUST_NOT_BE_EMPTY')
        if 'minute' in params:
            if not parser.parse('minute', 'string'):
                self.add_error('minute', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def update(self, data):
        crontab = Crontab.objects.get(pk=data['id'])
        if 'month' in data:
            crontab.month = data['month']
        if 'day' in data:
            crontab.day = data['day']
        if 'hour' in data:
            crontab.hour = data['hour']
        if 'minute' in data:
            crontab.minute = data['minute']
        if 'command_id' in data:
            crontab.command_id = data['command_id']
        if 'num_process' in data:
            crontab.num_process = data['num_process']
        crontab.save()
        return crontab


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        crontab = Crontab.objects.get(pk=data['id'])
        crontab.delete()
        return 1
