import json

class AbstractContainer(object):
    def __init__(self):
        pass
    def build(self):
        pass
    def boot_action(self, action, request, **kwargs):
        pass

class BaseContainer(AbstractContainer):
    def __init__(self):
        super(BaseContainer, self).__init__()
        self.request = None
        self.action = None
    def extract_params(self, request, **kwargs):
        params = {}
        for k in request.GET.iterkeys():
            params[k] = request.GET.get(k)
        for k in request.POST.iterkeys():
            if k.endswith('[]'):
                params[k[:(len(k)-2)]] = request.POST.getlist(k)
            else:
                params[k] = request.POST.get(k)
        for k in kwargs:
            params[k] = kwargs[k]
        return params
    def boot_action(self, action, request, **kwargs):
        action.set_request(request)
        action.set_params(self.extract_params(request, **kwargs))
        self.request = request
        self.action = action

# Import containers
import standard
