import json
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from notasquare.urad_api.containers.standard import Container
from application.models import *
from django.conf import settings
from application.modules.common import helpers

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        api = helpers.KubernetesAPI()
        response = api.GET('api/v1/namespaces/genopedia-test/pods/genopedia-job-manager-process-20')
        print json.dumps(json.loads(response), indent=4)
