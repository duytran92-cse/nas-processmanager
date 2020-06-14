import json, traceback
from django.views.generic import TemplateView
from django.conf import settings
from django.utils.module_loading import import_string
from django.http import JsonResponse

class AbstractHandler(TemplateView):
    def __init__(self):
        self.container = None
        self.request = None
        self.params = {}
    def init(self):
        self.create_container()
    def set_params(self, params):
        self.params = params
    def set_request(self, request):
        self.request = request
    def create_container(self):
        klass = import_string(settings.NOTASQUARE_URAD_CONTAINER)
        self.container = klass()
        self.container.build()
    def get_container(self):
        return self.container


class GETHandler(AbstractHandler):
    def __init__(self):
        super(GETHandler, self).__init__()
    def GET(self, params):
        return ('ok', {})
    def get(self, request, **kwargs):
        try:
            self.init()
            self.get_container().boot_handler(self, request, **kwargs)

            (status, dataset) = self.GET(self.params)
            return JsonResponse({
                'status': status,
                'data':   dataset
            })
        except Exception as e:
            return JsonResponse({
                'status': 'exception',
                'data':   {
                    'message': str(e)
                }
            })

class POSTHandler(AbstractHandler):
    def __init__(self):
        super(POSTHandler, self).__init__()
        self.form = None
    def POST(self, params):
        return ('ok', {})
    def post(self, request, **kwargs):
        try:
            self.init()
            self.get_container().boot_handler(self, request, **kwargs)

            (status, dataset) = self.POST(self.params)
            return JsonResponse({
                'status': status,
                'data':   dataset
            })
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({
                'status': 'exception',
                'data':   {
                    'message': str(e)
                }
            })

# Include common handlers
import standard
