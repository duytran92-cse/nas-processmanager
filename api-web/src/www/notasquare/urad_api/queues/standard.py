import json, time
from notasquare.urad_api.queues import BaseQueue
from django.conf import settings
from django.apps import apps as django_apps
from django.utils import timezone

class SimpleQueue(BaseQueue):
    def __init__(self):
        super(SimpleQueue, self).__init__()
        self.Job = django_apps.get_model('urad_api.Job')
        self.JobMessage = django_apps.get_model('urad_api.JobMessage')
    def load(self):
        pass
    def create_job(self, job_kind, parameters):
        job = self.Job()
        job.kind = job_kind
        job.parameters = json.dumps(parameters)
        job.status = 'open'
        job.save()
        return job.id
    def get_job(self, job_id):
        try:
            return self.Job.objects.get(pk=job_id)
        except:
            pass
        return None
    def has_job(self, kind):
        return self.Job.objects.filter(kind=kind).count() > 0
    def get_jobs(self, status=['open', 'in_progress'], kind=''):
        query = self.Job.objects
        if not status:
            query = query.filter(status__in=status)
        if kind != '':
            query = query.filter(kind=kind)
        return query.all()
    def pull_jobs(self, kind, N=1):
        data = []
        jobs = self.Job.objects.filter(status='open').filter(kind=kind).all()[:N]
        for job in jobs:
            data.append({
                'id':         job.id,
                'parameters': json.loads(job.parameters)
            })
            job.status = 'in_progress'
            job.save()
        return data
    def update_job_result(self, job_id, result):
        job = self.get_job(job_id)
        job.result = json.dumps(result)
        job.last_updated = timezone.now()
        job.save()
    def update_job_status(self, job_id, status):
        job = self.get_job(job_id)
        job.status = status
        job.last_updated = timezone.now()
        job.save()
    def update_job_message(self, job_id, message):
        job_message = self.JobMessage()
        job_message.job_id = job_id
        job_message.message = message
        job_message.save()
        job = self.get_job(job_id)
        job.last_updated = timezone.now()
        job.last_message = message
        job.save()
