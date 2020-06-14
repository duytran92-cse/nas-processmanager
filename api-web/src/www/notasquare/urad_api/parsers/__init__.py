
class AbstractParser(object):
    def __init__(self):
        self.params = {}
        self.data = {}
    def set_params(self, params):
        self.params = params
    def parse(self, key = '', kind='string'):
        return None
    def get_data(self):
        return self.data

class BaseParser(AbstractParser):
    pass

import standard
