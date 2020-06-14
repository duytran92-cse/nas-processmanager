from notasquare.urad_api.consumers import BaseConsumer

class Consumer(BaseConsumer):
    def __init__(self):
        super(Consumer, self).__init__()
        self.container = None
        self.queue = None
    def set_container(self, container):
        self.container = container
        self.queue = container.get_queue()
    def update_job_result(self, job_id, result):
        self.queue.update_job_result(job_id, result)
    def update_job_status(self, job_id, status):
        self.queue.update_job_status(job_id, status)
    def update_job_message(self, job_id, message):
        self.queue.update_job_message(job_id, message)
    def pull_one_job(self, kind=''):
        jobs = self.queue.pull_jobs(kind, N=1)
        if len(jobs) == 0:
            return None
        return jobs[0]
    def pull_jobs(self, kind, N):
        return self.queue.pull_jobs(kind, N)
    def execute(self):
        pass
