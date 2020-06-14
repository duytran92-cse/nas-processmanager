import json
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from notasquare.urad_api.containers.standard import Container
from application.models import *
from django.conf import settings
from application.modules.common import helpers

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        processes = Process.objects.all()
        print "Delete %s process(s)" % (len(processes))

        for p in processes:
            try:
                api = helpers.KubernetesAPI()
                api.DELETE('api/v1/namespaces/genopedia-test/pods/%s' % (p.pod_id))
                print "  --> %s" % (p.pod_id)
                p.delete()
            except:
                pass
