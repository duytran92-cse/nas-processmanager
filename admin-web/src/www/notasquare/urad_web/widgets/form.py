from notasquare.urad_web.widgets import BaseWidget

class Form(BaseWidget):
    def __init__(self):
        super(Form, self).__init__()
        self.title = ''
        self.tabs = []
        self.active_tab = ''
        self.fields = {}
        self.messages = []
        self.buttons = []
    def set_title(self, title):
        self.title = title
    def add_field(self, field):
        self.fields[field.id] = field
    def set_form_data(self, form_data):
        for k in form_data:
            if k in self.fields:
                self.fields[k].set_data(form_data[k])
    def parse_from_params(self, params):
        for k in self.fields:
            self.fields[k].parse_param(params)        
    def get_form_data(self):
        data = {}
        for k in self.fields:
            data[k] = self.fields[k].get_data()
        return data
    def add_message(self, type='info', message=''):
        self.messages.append({'type': type, 'message': message})
    def add_tab(self, id, label, url):
        self.tabs.append({
            'id':      id,
            'label':   label,
            'url':     url
        })
    def set_active_tab(self, id):
        self.active_tab = id
    def add_button(self, id, label, iclass=''):
        self.buttons.append({
            'id':     id,
            'label':  label,
            'class':  iclass
        })
    def set_field_errors(self, id, field_errors):
        if id in self.fields:
            self.fields[id].set_errors(field_errors)
    def has_error(self):
        for id in self.field_errors:
            if len(self.field_errors[id]) > 0:
                return True
        return False
