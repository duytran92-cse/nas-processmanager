
class AbstractQueue(object):
    def create_job(self, job_kind, parameters):
        pass
    def get_job(self, job_id):
        pass
    def has_job(self, job_kind):
        pass
    def get_jobs(self, status, job_kind):
        pass
    def pull_jobs(self, job_kind, N=1):
        pass
    def update_job_result(self, job_id, result):
        pass
    def update_job_status(self, job_id, status):
        pass
    def update_job_message(self, job_id, message):
        pass

class BaseQueue(AbstractQueue):
    pass

import standard
