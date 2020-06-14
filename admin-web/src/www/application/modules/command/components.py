from django.conf import settings
from application.modules.common import page_contexts

class CommandStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        params['_pager_start'] = (page_number - 1) * 100
        params['_pager_num'] = 100
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.JOB_MANAGER_API_URL + '/command/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.JOB_MANAGER_API_URL + '/command/get', GET={'id': id})
    def create(self, data):
        return self.container.call_api(settings.JOB_MANAGER_API_URL + '/command/create', POST=data)
    def update(self, data, id):
        data['id'] = id
        return self.container.call_api(settings.JOB_MANAGER_API_URL + '/command/update', POST=data)
    def invoke(self, id):
        return self.container.call_api(settings.JOB_MANAGER_API_URL + '/command/invoke', POST={'id': id})
    def delete(self, id):
        return self.container.call_api(settings.JOB_MANAGER_API_URL + '/command/delete', POST={'id': id})
    def populate_combobox(self, kind=''):
        choices = []
        params = {}
        params['_sort_key'] = 'name'
        params['_sort_dir'] = 'asc'
        records = self.container.call_api(settings.JOB_MANAGER_API_URL + '/command/list', GET=params)
        for record in records['data']['records']:
            choices.append({
                'id':     record['id'],
                'label':  record['name']
            })
        return choices
