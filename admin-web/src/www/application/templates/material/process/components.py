from django.conf import settings
from application.modules.common import page_contexts

class ProcessStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        params['_pager_start'] = (page_number - 1) * 100
        params['_pager_num'] = 100
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.JOB_MANAGER_API_URL + '/process/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.JOB_MANAGER_API_URL + '/process/get', GET={'id': id})

    def get_log(self, id):
        return self.container.call_api(settings.JOB_MANAGER_API_URL + '/process/get_log', GET={'id': id})

    def stop(self, id):
        return self.container.call_api(settings.JOB_MANAGER_API_URL + '/process/stop', GET={'id': id})

    def clean_all(self, params={}):
        return self.container.call_api(settings.JOB_MANAGER_API_URL + '/process/clean_all', GET=params)

class ProcessFullPageContext(page_contexts.FullPageContext):
    def __init__(self, params, container):
        super(ProcessFullPageContext, self).__init__()
        self.page_title = 'Process'
        self.menu.set_group_selected('process')
        self.breadcrumb.add_entry('process', 'Process', '/process/list')