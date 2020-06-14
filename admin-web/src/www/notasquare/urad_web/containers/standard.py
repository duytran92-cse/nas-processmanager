import django, logging, notasquare, urllib, urllib2, json
from django.forms.models import model_to_dict
from notasquare.urad_web.containers import BaseContainer
from notasquare.urad_web import *

class Container(BaseContainer):
    def __init__(self):
        super(Container, self).__init__()
        self.settings = django.conf.settings
    def get_settings(self):
        return self.settings
    def get_request(self):
        return self.request
    def get_session(self):
        return self.request.session
    def call_api(self, url, POST=None, GET={}):
        if POST is not None:
            req = urllib2.Request(url, json.dumps(POST))
            res = urllib2.urlopen(req)
            data = json.loads(res.read())
            return data
        else:
            res = urllib.urlopen(url + '?' + urllib.urlencode(GET))
            data = res.read()
            data = json.loads(data)
            return data
