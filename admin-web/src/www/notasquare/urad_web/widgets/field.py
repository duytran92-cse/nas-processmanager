from notasquare.urad_web.widgets import BaseWidget


class Field(BaseWidget):
    def __init__(self, id):
        super(Field, self).__init__()
        self.id = id
        self.data = ''
        self.label = ''
        self.is_required = False
        self.errors = []
    def set_errors(self, errors):
        self.errors = errors
    def set_data(self, data):
        self.data = data
    def get_data(self):
        return self.data
    def parse_param(self, params):
        if self.id in params:
            self.data = str(params[self.id]).strip()


class Textbox(Field):
    code = 'textbox'


class Textarea(Field):
    code = 'textarea'


class Richtext(Field):
    code = 'richtext'


class Combobox(Field):
    code = 'combobox'
    def __init__(self, id, choices=[], blank=False):
        super(Combobox, self).__init__(id)
        if blank:
            self.choices = [{'id': '', 'label': ''}] + choices
        else:
            self.choices = choices
    def set_choices(self, choices):
        self.choices = choices


class MultipleChoice(Field):
    code = 'multiple_choice'
    def __init__(self, id, choices=[]):
        super(MultipleChoice, self).__init__(id)
        self.choices = choices
    def set_choices(self, choices):
        self.choices = choices
    def parse_param(self, params):
        self.data = []
        if self.id in params:
            for v in params[self.id]:
                self.data.append(int(v))


class Collection(Field):
    code = 'collection'
    def __init__(self, id, fields=[]):
        super(Collection, self).__init__(id)
        self.fields = fields
    def set_fields(self, fields):
        self.fields = fields


class List(Field):
    code = 'list'
    def __init__(self, id, fields={}):
        super(List, self).__init__(id)
        self.fields = fields
    def set_fields(self, fields):
        self.fields = fields
    def parse_param(self, params):
        sort_order_field_id = self.id + '_sort_order'
        if sort_order_field_id in params:
            self.data = []
            sort_orders = params[sort_order_field_id].split(',')
            for index in sort_orders:
                if index.strip() != '':
                    record = {}
                    for field_id in self.fields:
                        field_key = field_id + '_' + str(index)
                        record[field_id] = params[field_key] if field_key in params else ''
                    self.data.append(record)
