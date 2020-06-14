import django, logging, notasquare, urllib, urllib2, json
from django.forms.models import model_to_dict
from notasquare.urad_api.containers import BaseContainer
from notasquare.urad_api import *

class Container(BaseContainer):
    def __init__(self):
        super(Container, self).__init__()
        self.settings = django.conf.settings
        self.queue = None
        self.authenticator = None
        self.authorizator = None
    def create_parser(self, params):
        parser = parsers.standard.Parser()
        parser.set_params(params)
        return parser
    def get_authenticator(self):
        if self.authenticator == None:
            self.authenticator = authenticators.standard.TestAuthenticator()
        return self.authenticator
    def get_authorizator(self):
        if self.authorizator == None:
            self.authorizator = authorizators.rbac.RbacAuthorizator()
            self.authorizator.load_security(self.settings.NOTASQUARE_RBAC_AUTHORIZATOR_SECURITY_CLASS)
        return self.authorizator
    def get_logger(self, name='default'):
        logger = logging.getLogger(name)
        return logger
    def get_queue(self):
        if self.queue == None:
            self.queue = queues.standard.SimpleQueue()
            self.queue.load()
        return self.queue
    def get_user(self):
        return self.create_authorizator().get_user()
    def get_cache(self):
        pass
    def get_settings(self):
        return self.settings
    def model_to_dict(self, model):
        return model_to_dict(model)
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

container = Container()
