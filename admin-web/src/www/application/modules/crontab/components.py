from django.conf import settings
from application.modules.common import page_contexts

class CrontabStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        params['_pager_start'] = (page_number - 1) * 100
        params['_pager_num'] = 100
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.JOB_MANAGER_API_URL + '/crontab/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.JOB_MANAGER_API_URL + '/crontab/get', GET={'id': id})
    def create(self, data):
        return self.container.call_api(settings.JOB_MANAGER_API_URL + '/crontab/create', POST=data)
    def update(self, data, id):
        data['id'] = id
        return self.container.call_api(settings.JOB_MANAGER_API_URL + '/crontab/update', POST=data)
    def delete(self, id):
        return self.container.call_api(settings.JOB_MANAGER_API_URL + '/crontab/delete', POST={'id': id})
