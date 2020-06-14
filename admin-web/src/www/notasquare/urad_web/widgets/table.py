import math
from notasquare.urad_web.widgets import BaseWidget

class Table(BaseWidget):
    class Column(object):
        name   = ''
        title  = ''
        width  = ''
        sortable = False
        sort_dir  = ''
    class Button(object):
        name   = ''
        url    = ''
        iclass = ''
    def __init__(self):
        super(Table, self).__init__()
        self.title = ''
        self.subtitle = ''
        self.columns = []
        self.buttons = []
        self.data = []
    def set_title(self, title):
        self.title = title
    def set_subtitle(self, subtitle):
        self.subtitle = subtitle
    def create_column(self, name, title, width='20%', sortable=False):
        column = self.Column()
        column.name = name
        column.title = title
        column.width = width
        column.sortable = sortable
        self.columns.append(column)
        return column
    def create_button(self, name, url, iclass=''):
        button = self.Button()
        button.name = name
        button.url = url
        button.iclass = iclass
        self.buttons.append(button)
        return button
    def set_data(self, data):
        self.data = data

class DataTable(Table):
    def __init__(self):
        super(DataTable, self).__init__()
        self.current_page = 1
        self.total_pages = 1
        self.record_per_page = 10
        self.total_records = 15
        self.fields = {}
        self.messages = []
    def set_current_page(self, current_page):
        self.current_page = current_page
    def set_total_pages(self, total_pages):
        self.total_pages = total_pages
    def set_total_records(self, total_records):
        self.total_records = total_records
        self.total_pages = int(math.ceil(self.total_records * 1.0 / self.record_per_page))
    def set_table_form_data(self, table_form_data):
        self.set_form_data(table_form_data)
    def set_sort(self, sort_key, sort_dir):
        for c in self.columns:
            if c.name == sort_key:
                c.sort_dir = sort_dir
    def add_field(self, field):
        self.fields[field.id] = field
    def set_form_data(self, form_data):
        for k in form_data:
            if k in self.fields:
                self.fields[k].set_data(form_data[k])
    def parse_from_params(self, params):
        for k in params:
            if k in self.fields:
                self.fields[k].parse_param(params[k])
    def get_form_data(self):
        data = {}
        for k in self.fields:
            data[k] = self.fields[k].get_data()
        return data
    def add_message(self, type='info', message=''):
        self.messages.append({'type': type, 'message': message})
