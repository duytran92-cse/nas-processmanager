
class AbstractAuthorizator(object):
    def set_user(self, user):
        pass
    def get_user(self):
        pass
    def is_authorized(self, user, resource):
        pass

class BaseAuthorizator(AbstractAuthorizator):
    def __init__(self):
        self.user = None
    def set_user(self, user):
        self.user = user
    def get_user(self):
        return self.user

import rbac
