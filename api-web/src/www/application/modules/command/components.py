from application.models import *
from application.modules.common import helpers
from django.conf import settings
import time

class Helper(object):
    def invoke_command(self, command):
        api = helpers.KubernetesAPI()
        process = Process()
        process.command_id = command.id
        process.save()
        process.pod_id = '%s-%s' % (settings.PROCESS_BASE_NAME, process.id)
        process.namespace = command.namespace
        process.save()
        #
        command_id = process.command_id
        commandvariable = CommandVariable.objects.filter(command_id=command_id).all()
        env = []
        for var in commandvariable:
            if var.name == '' or var.value == '':
                continue
            env.append({'name': str(var.name), 'value': str(var.value)})
        print 'env: %s | pod_id: %s' %(env, process.pod_id)
        try:
            response = api.POST('api/v1/namespaces/%s/pods' % (command.namespace), {
                'kind': 'Pod',
                'metadata': {
                    'namespace': command.namespace,
                    'name': process.pod_id,
                },
                'spec': {
                    'containers': [
                        {
                            'name': 'default-container',
                            'image': command.docker_image,
                            'command': self.parse_token(command.exec_command),
                            'args': self.parse_token(command.exec_args),
                            'resources': {
                                'requests': {
                                    'cpu': '%sm' % (command.cpu_request),
                                    'memory': '%sMi' % (command.mem_request)
                                },
                                'limits': {
                                    'cpu': '%sm' % (command.cpu_limit),
                                    'memory': '%sMi' % (command.mem_limit)
                                }
                            },
                            'env': env
                        }
                    ],
                    'restartPolicy': 'Never'
                }
            })
            process.pod_creation_log = response
            process.save()
            return process

        except:
            return process

    def follow_stream(self, process):
        api = helpers.KubernetesAPI()
        #url_pod = 'api/v1/namespaces/%s/pods/%s/log' %('genopedia-test', 'process-manager-test-10')
        url_pod = 'api/v1/namespaces/%s/pods/%s/log' % (process.namespace, process.pod_id)
        response = api.GET(url_pod, {
            'pretty': 'true',
            'sinceSeconds': 15*60
        })
        print 'Log: %s' % (response)
        return response

    def parse_token(self, token):
        return token.split(' ')
