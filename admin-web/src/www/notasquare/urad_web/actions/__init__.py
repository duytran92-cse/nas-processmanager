import json, traceback
from django.views.generic import TemplateView
from django.conf import settings
from django.utils.module_loading import import_string
from django.http import JsonResponse, HttpResponse

class AbstractAction(TemplateView):
    def __init__(self):
        self.container = None
        self.request = None
        self.params = {}
    def init(self):
        self.create_container()
        global container
        container = self.container
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
    def get(self, request, **kwargs):
        self.init()
        self.container.boot_action(self, request, **kwargs)
        return self.GET()
    def GET(self):
        return HttpResponse("")
    def post(self, request, **kwargs):
        self.init()
        self.container.boot_action(self, request, **kwargs)
        return self.POST()
    def POST(self):
        return HttpResponse("")

class BaseAction(AbstractAction):
    def create_page_context(self):
        return self.container.get_default_page_context()
    def get_action_name(self):
        request = self.get_container().get_request()
        return request.resolver_match.url_name

import crud
