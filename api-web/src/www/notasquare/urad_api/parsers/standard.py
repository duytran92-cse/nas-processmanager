from notasquare.urad_api.parsers import BaseParser

class Parser(BaseParser):
    def __init__(self):
        super(Parser, self).__init__()
        self.handlers = {
            'string':  self.parse_string,
            'integer': self.parse_integer,
            'model':   self.parse_model,
            'array':   self.parse_array
        }
        self.params = {}
    def set_params(self, params):
        self.params = params
        self.data = params
    def parse(self, key = '', kind = 'string', **kwargs):
        if key not in self.params:
            return None
        if kind not in self.handlers:
            raise Exception("Undefined parser: " + str(kind))
        handler = self.handlers[kind]
        value = handler(self.params[key], **kwargs)
        self.data[key] = value
        return value
    def parse_string(self, param):
        return str(param).strip()
    def parse_integer(self, param):
        try:
            return int(param)
        except:
            return None
    def parse_model(self, param, model):
        try:
            return model.objects.get(pk=param)
        except:
            return None
    def parse_array(self, param, entry_parser):
        try:
            arr = []
            for entry in param:
                arr.append(entry_parser(entry))
            return arr
        except:
            return None
