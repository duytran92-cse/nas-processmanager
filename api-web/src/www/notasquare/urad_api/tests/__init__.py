import json
from django.utils.module_loading import import_string
from django.conf import settings
from django.test import TestCase, Client

class BaseUnitTest(TestCase):
    def init(self):
        self.client = Client()
        self.headers = {}
        self.create_container()
    def create_container(self):
        klass = import_string(settings.NOTASQUARE_URAD_TEST_CONTAINER)
        self.container = klass()
        self.container.build()
    def set_headers(self, headers = {}):
        self.headers = headers
    def get(self, message = '', url = ''):
        print "\n"
        print "********************************************"
        print "[x] " + message
        print "GET: " + url
        response = self.client.get(url, **self.headers)
        print "RESPONSE: "
        print response
        print "\n"
        print "DATA:"
        print json.dumps(json.loads(response.content), indent=4)
        print "\n"
    def post(self, message = '', url = '', data = {}):
        print "\n"
        print "********************************************"
        print "[x] " + message
        print "GET: " + url
        response = self.client.post(url, json.dumps(data), content_type="application/json", **self.headers)
        print "RESPONSE: "
        print response
        print "\n"
        print "DATA:"
        print json.dumps(json.loads(response.content), indent=4)
        print "\n"
    def run_consumer_test(self, kind, parameters_set, consumer):
        queue = self.container.get_queue()
        for parameters in parameters_set:
            queue.create_job(kind, parameters)
        print "\n"
        print "********************************************"
        print "[x] CONSUMER: " + consumer.__class__.__name__
        consumer.set_container(self.container)
        consumer.execute()
        print "DONE.."
        jobs = queue.get_jobs(status=['done', 'error'], kind=kind)
        for job in jobs:
            print "\n"
            print "JOB (id=" + str(job.id) + ")"
            print "   KIND:       " + str(job.kind)
            print "   STATUS:     " + str(job.status)
            print "   PARAMETERS: " + job.parameters
            print "   RESULT:     " + job.result
            print "   LAST MSG:   " + job.last_message
