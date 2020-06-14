from django.http import JsonResponse
from django.forms.models import model_to_dict
from notasquare.urad_api import parsers
from notasquare.urad_api.handlers import GETHandler, POSTHandler


class GetHandler(GETHandler):
    def __init__(self):
        super(GetHandler, self).__init__()
    def parse_and_validate(self, params):
        return params
    def get_data(self, data):
        return {}
    def GET(self, params):
        data = self.parse_and_validate(params)
        return ('ok', {'record': self.get_data(data)})

class ListHandler(GETHandler):
    def __init__(self):
        super(ListHandler, self).__init__()
    def parse_and_validate(self, params):
        return params
    def extract_sort_params(self, params):
        sort_key = params['_sort_key'] if '_sort_key' in params else 'id'
        sort_dir = params['_sort_dir'] if '_sort_dir' in params else 'desc'
        return (sort_key, sort_dir)
    def extract_pager_params(self, params):
        pager_start = int(params['_pager_start']) if '_pager_start' in params else 0
        pager_num = int(params['_pager_num']) if '_pager_num' in params else 100
        return (pager_start, pager_num)
    def create_query(self, params):
        pass
    def build_sort_part(self, query, sort_key, sort_dir):
        key = sort_key
        if sort_dir == 'desc':
            key = '-' + key
        query = query.order_by(key)
        return query
    def serialize_entry(self, entry):
        return model_to_dict(entry)
    def GET(self, params):
        params = self.parse_and_validate(params)
        (sort_key, sort_dir) = self.extract_sort_params(params)
        (pager_start, pager_num) = self.extract_pager_params(params)

        query = self.create_query(params)
        query = self.build_sort_part(query, sort_key, sort_dir)
        dataset = []
        start = pager_start
        end = pager_start + pager_num
        for entry in query.all()[start:end]:
            dataset.append(self.serialize_entry(entry))

        query = self.create_query(params)
        total_matched = query.count()

        return ('ok', {
            'records': dataset,
            'total_matched': total_matched
        })


class FormHandler(POSTHandler):
    def __init__(self):
        super(FormHandler, self).__init__()
        self.data = {}
        self.errors = {}
        self.response_data = {}
        self.parser = None
    def build(self):
        pass
    def parse_and_validate(self, params):
        return params
    def add_error(self, key, err):
        if not key in self.errors:
            self.errors[key] = []
        self.errors[key].append(err)
    def has_errors(self):
        for k in self.errors:
            if len(self.errors[k]) > 0:
                return True
        return False
    def on_success(self):
        pass
    def set_response_data(self, response_data):
        self.response_data = response_data
    def get_response_data(self):
        return self.response_data
    def POST(self, params):
        self.data = self.parse_and_validate(params)
        if self.has_errors():
            return ('error', {'errors': self.errors})
        self.on_success()
        if self.has_errors():
            return ('error', {'errors': self.errors})
        return ('ok', self.get_response_data())


class CreateHandler(FormHandler):
    def __init__(self):
        super(CreateHandler, self).__init__()
    def create(self, data):
        pass
    def on_success(self):
        obj = self.create(self.data)
        self.set_response_data({'pk': obj.id})


class UpdateHandler(FormHandler):
    def __init__(self):
        super(UpdateHandler, self).__init__()
    def update(self, data):
        pass
    def on_success(self):
        obj = self.update(self.data)
        self.set_response_data({'pk': obj.id})


class DeleteHandler(FormHandler):
    def __init__(self):
        super(DeleteHandler, self).__init__()
    def delete(self, data):
        pass
    def on_success(self):
        num_record_deleted = self.delete(self.data)
        self.set_response_data({'num_record_deleted': num_record_deleted})
