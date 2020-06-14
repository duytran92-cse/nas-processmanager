from notasquare.urad_api import *
from application.models import *
from application import constants
from . import components

class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = Command.objects
        if 'text' in data:
            query = query.filter(name__contains=data['text'])
        return query
    def serialize_entry(self, command):
        return {
            'id':                 command.id,
            'name':               command.name,
            'namespace':          command.namespace,
            'docker_image':       command.docker_image,
            'exec_command':       command.exec_command,
            'exec_args':          command.exec_args,
            'cpu_request':        command.cpu_request,
            'cpu_limit':          command.cpu_limit,
            'mem_request':        command.mem_request,
            'mem_limit':          command.mem_limit,
            'timeout':            command.timeout
        }


class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        command = Command.objects.get(pk=data['id'])

        variables = []
        records = CommandVariable.objects.filter(command_id=command.id).all()
        for r in records:
            variables.append({
                'name':    r.name,
                'value':   r.value
            })

        result = {}
        result['id'] = command.id
        result['name'] = command.name
        result['namespace'] = command.namespace
        result['docker_image'] = command.docker_image
        result['exec_command'] = command.exec_command
        result['exec_args'] = command.exec_args
        result['cpu_request'] = command.cpu_request
        result['cpu_limit'] = command.cpu_limit
        result['mem_request'] = command.mem_request
        result['mem_limit'] = command.mem_limit
        result['timeout'] = command.timeout
        result['variables'] = variables
        return result


class Create(handlers.standard.CreateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('name', 'string'):
            self.add_error('name', 'MUST_NOT_BE_EMPTY')
        if not parser.parse('namespace', 'string'):
            self.add_error('namespace', 'MUST_NOT_BE_EMPTY')
        if not parser.parse('docker_image', 'string'):
            self.add_error('docker_image', 'MUST_NOT_BE_EMPTY')
        if not parser.parse('exec_command', 'string'):
            self.add_error('exec_command', 'MUST_NOT_BE_EMPTY')
        if not parser.parse('cpu_request', 'integer'):
            self.add_error('cpu_request', 'MUST_NOT_BE_EMPTY')
        if not parser.parse('cpu_limit', 'integer'):
            self.add_error('cpu_limit', 'MUST_NOT_BE_EMPTY')
        if not parser.parse('mem_request', 'integer'):
            self.add_error('mem_request', 'MUST_NOT_BE_EMPTY')
        if not parser.parse('mem_limit', 'integer'):
            self.add_error('mem_limit', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def create(self, data):
        command = Command()
        command.name = data['name']
        command.namespace = data['namespace']
        command.docker_image = data['docker_image']
        command.exec_command = data['exec_command']
        if 'exec_args' in data:
            command.exec_args = data['exec_args']
        command.cpu_request = data['cpu_request']
        command.cpu_limit = data['cpu_limit']
        command.mem_request = data['mem_request']
        command.mem_limit = data['mem_limit']
        command.timeout = data['timeout']
        command.save()

        if 'variables' in data:
            for r in data['variables']:
                variable = CommandVariable()
                variable.command_id = command.id
                variable.name = r['name']
                variable.value = r['value']
                variable.save()

        return command


class Update(handlers.standard.UpdateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if 'name' in params:
            if not parser.parse('name', 'string'):
                self.add_error('name', 'MUST_NOT_BE_EMPTY')
        if 'namespace' in params:
            if not parser.parse('namespace', 'string'):
                self.add_error('namespace', 'MUST_NOT_BE_EMPTY')
        if 'docker_image' in params:
            if not parser.parse('docker_image', 'string'):
                self.add_error('docker_image', 'MUST_NOT_BE_EMPTY')
        if 'exec_command' in params:
            if not parser.parse('exec_command', 'string'):
                self.add_error('exec_command', 'MUST_NOT_BE_EMPTY')
        if 'cpu_request' in params:
            if not parser.parse('cpu_request', 'integer'):
                self.add_error('cpu_request', 'MUST_NOT_BE_EMPTY')
        if 'cpu_limit' in params:
            if not parser.parse('cpu_limit', 'integer'):
                self.add_error('cpu_limit', 'MUST_NOT_BE_EMPTY')
        if 'mem_request' in params:
            if not parser.parse('mem_request', 'integer'):
                self.add_error('mem_request', 'MUST_NOT_BE_EMPTY')
        if 'mem_limit' in params:
            if not parser.parse('mem_limit', 'integer'):
                self.add_error('mem_limit', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def update(self, data):
        command = Command.objects.get(pk=data['id'])
        if 'name' in data:
            command.name = data['name']
        if 'namespace' in data:
            command.namespace = data['namespace']
        if 'docker_image' in data:
            command.docker_image = data['docker_image']
        if 'exec_command' in data:
            command.exec_command = data['exec_command']
        if 'exec_args' in data:
            command.exec_args = data['exec_args']
        if 'cpu_request' in data:
            command.cpu_request = data['cpu_request']
        if 'cpu_limit' in data:
            command.cpu_limit = data['cpu_limit']
        if 'mem_request' in data:
            command.mem_request = data['mem_request']
        if 'mem_limit' in data:
            command.mem_limit = data['mem_limit']
        if 'timeout' in data:
            command.timeout = data['timeout']
        command.save()

        if 'variables' in data:
            CommandVariable.objects.filter(command_id=command.id).delete()
            for r in data['variables']:
                variable = CommandVariable()
                variable.command_id = command.id
                variable.name = r['name']
                variable.value = r['value']
                variable.save()

        return command

class Invoke(handlers.standard.CreateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        return parser.get_data()
    def create(self, data):
        command = Command.objects.get(pk=data['id'])
        process = components.Helper().invoke_command(command)
        return process

class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        command = Command.objects.get(pk=data['id'])
        command.delete()
        return 1
