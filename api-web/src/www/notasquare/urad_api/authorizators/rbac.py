from django.utils.module_loading import import_string
from notasquare.urad_api.authorizators import BaseAuthorizator

class RbacAuthorizator(BaseAuthorizator):
    def __init__(self):
        super(RbacAuthorizator, self).__init__()
        self.group_authorization = {}
    def load_security(self, classname=''):
        klass = import_string(classname)
        for key in klass.__dict__.keys():
            if not key.startswith('__'):
                self.group_authorization[key] = klass.__dict__[key]
    def is_authorized(self, user, handler):
        current_urlname = handler.request.resolver_match.url_name
        for group in user.groups:
            if group in self.group_authorization:
                if current_urlname in self.group_authorization[group]:
                    return True
        return False
