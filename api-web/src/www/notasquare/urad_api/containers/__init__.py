import json

class AbstractContainer(object):
    def __init__(self):
        pass
    def build(self):
        pass
    def create_authenticator(self):
        pass
    def create_authorizator(self):
        pass
    def boot_handler(self, handler, request, **kwargs):
        pass

class BaseContainer(AbstractContainer):
    def extract_params(self, request, **kwargs):
        params = {}
        for k in request.GET.iterkeys():
            params[k] = request.GET.get(k)
        try:
            req = json.loads(request.body)
            for k in req:
                params[k] = req[k]
        except:
            pass
        for k in kwargs:
            params[k] = kwargs[k]
        return params
    def boot_handler(self, handler, request, **kwargs):
        params = self.extract_params(request, **kwargs)
        handler.set_request(request)
        handler.set_params(params)
        authenticator = self.get_authenticator()
        user = authenticator.parse_user(request)
        authorizator = self.get_authorizator()
        authorizator.set_user(user)
        if not authorizator.is_authorized(user, handler):
            raise Exception('Unauthorized access')

# Import containers
import standard
