import json, threading, time, sys
import urllib2
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from notasquare.urad_api.containers.standard import Container
from application import models
from django.conf import settings
from application.modules.common import helpers
from application.modules.common import time_custom
from application.modules.command.components import Helper


class Command(BaseCommand):
    def print_log(self, service, message):
        print '[%s] %s - %s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), service, message)

    def convert_time_crontab(self, dict_value):
        _temp = {}
        for key in dict_value.iterkeys():
            if key not in ['hour', 'minute', 'day', 'month']:
                _temp[key] = dict_value[key]
            else:
                _temp[key] = helpers.parse(str(dict_value[key]), 0)
        return _temp

    def update_process(self):
        api = helpers.KubernetesAPI()
        while True:
            # delete pod beacause status=stop
            processes_stop = models.Process.objects.filter(status__in=['Stop', 'Terminated']).all()
            for p in processes_stop:
                try:
                    api.DELETE('api/v1/namespaces/%s/pods/%s' % (p.namespace, p.pod_id))
                    print 'Deleted pod on kube'
                except:
                    pass
            #
            processes = models.Process.objects.filter(status__in=['', 'Pending', 'Running']).all()
            self.print_log('Update Process', "Update %s process(s)" % (len(processes)))

            for p in processes:
                #print 'Follow stream'
                #print Helper().follow_stream(p)
                #print 'Done stream'

                command_timeout = models.Command.objects.get(pk=p.command_id).timeout
                timestamp = p.timestamp

                # timeout = 0, disable timeout
                #
                if command_timeout != 0 and time_custom.compare_time(time_start=timestamp) > command_timeout:

                    p.message = 'Timeout'
                    p.status = 'Stop'
                    p.save()
                    try:
                        api.DELETE('api/v1/namespaces/%s/pods/%s' % (p.namespace, p.pod_id))
                        print 'Deleted pod on kube'
                    except:
                        pass
                    #print 'Delete pod out of timeout: process_id = %s' % (p.id)
                    #p.delete()
                    continue
                try:
                    p.log = api.GET('api/v1/namespaces/%s/pods/%s/log' % (p.namespace, p.pod_id), {
                        'pretty': 'true',
                        'sinceSeconds': 15*60
                    })
                    p.save()
                except:
                    pass
                try:
                    self.print_log('Update Process', "    --> update %s" % (p.pod_id))
                    response = api.GET('api/v1/namespaces/%s/pods/%s' % (p.namespace, p.pod_id))
                    data = json.loads(response)
                    #print 'data: %s' %(data)
                    p.status = data['status']['phase']
                    if 'terminated' in data['status']['containerStatuses'][0]['state']:
                        d = data['status']['containerStatuses'][0]['state']['terminated']
                        if d['reason'] != 'Completed':
                            p.status = 'Terminated'
                        p.message = '%s at %s, exit code: %s' % (d['reason'], d['finishedAt'], d['exitCode'])
                    if 'waiting' in data['status']['containerStatuses'][0]['state']:
                        d = data['status']['containerStatuses'][0]['state']['waiting']
                        p.message = 'Waiting.. Reason: %s, Message: %s' % (d['reason'], d['message'])
                    if 'running' in data['status']['containerStatuses'][0]['state']:
                        p.message = p.log.split("\n").pop()
                    p.save()
                except Exception as e:
                    print 'Exception: %s' %(e)
                    p.message = str(e)
                    p.save()

            time.sleep(10)

    def serve_crontab(self):
        # iter_time: seconds
        iter_time = 60
        threading.Timer(iter_time, self.serve_crontab).start()
        self.print_log('Crontab', 'Serve crontab')

        print 'Get list crontab'
        list_crontab = models.Crontab.objects.all().values()
        print list_crontab

        for job in list_crontab:

            gm_time = time.gmtime()
            datetime_now = datetime(gm_time.tm_year, gm_time.tm_mon, gm_time.tm_mday, \
                                    gm_time.tm_hour, gm_time.tm_min)
            job = self.convert_time_crontab(job)
            if time_custom.is_run_job(job_dict=job, datetime_now=datetime_now, index=0):
                # run job --> process
                id = job.get('command_id')
                print 'Command id: %s| Cronjob id: %s' % (id, job.get('id'))
                command = models.Command.objects.get(pk=id)
                num_process = job.get('num_process')
                print 'Num process: %s' % (num_process)
                if num_process > 1:
                    for i in range(0, num_process):
                        Helper().invoke_command(command)
                else:
                    Helper().invoke_command(command)

    def handle_follow_stream(self):

        print 'Follow stream'
        print Helper().follow_stream()
        print 'Done stream'

    def handle(self, *args, **kwargs):
        threading.Thread(target=self.update_process).start()
        self.serve_crontab()

        while True:
            time.sleep(60)
