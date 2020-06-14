import json, urllib
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web.actions import BaseAction
from notasquare.urad_web import page_contexts, widgets
from notasquare.urad_web_material import renderers


class ListAction(BaseAction):
    def GET(self):
        subact = self.params['subact'] if 'subact' in self.params else ''
        if subact == 'change_page':
            self.change_page()
        if subact == 'clear_form':
            self.clear_form()
        if subact == 'change_sort':
            self.change_sort()
        return self.view_list_page()
    def POST(self):
        self.apply_filter()
        return self.view_list_page()
    def view_list_page(self):
        page_context = self.create_page_context()
        table = self.create_table()
        self.populate_table(table)
        page_context.add_widget(table)
        return HttpResponse(page_context.render())
    def create_table(self):
        pass
    def change_page(self):
        page_number = self.params['page']
        session = self.get_container().get_session()
        session_key = '%s_list_table_page_number' % (self.get_action_name())
        session[session_key] = int(page_number)
    def change_sort(self):
        sortkey = self.params['sortkey']
        sortdir = self.params['sortdir']
        session = self.get_container().get_session()
        session_key = '%s_list_table_sort' % (self.get_action_name())
        session[session_key] = (sortkey, sortdir)
    def clear_form(self):
        session = self.get_container().get_session()
        session_key = '%s_list_table_form' % (self.get_action_name())
        session[session_key] = {}
    def apply_filter(self):
        session = self.get_container().get_session()
        session_table_page_number = '%s_list_table_page_number' % (self.get_action_name())
        session[session_table_page_number] = 1
        session_table_form_key = '%s_list_table_form' % (self.get_action_name())
        session[session_table_form_key] = self.params
    def populate_table(self, table):
        page_number = self.get_page_number()
        table_form_data = self.get_table_form_data()
        (sortkey, sortdir) = self.get_table_sort()
        data = self.load_table_data(table_form_data, sortkey, sortdir, page_number)
        table.set_data(data['records'])
        table.set_total_records(data['total_matched'])
        table.set_table_form_data(table_form_data)
        table.set_current_page(page_number)
        table.set_sort(sortkey, sortdir)
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        return []
    def get_page_number(self):
        session = self.get_container().get_session()
        session_table_page_number = '%s_list_table_page_number' % (self.get_action_name())
        return session.get(session_table_page_number, 1)
    def get_table_form_data(self):
        session = self.get_container().get_session()
        session_table_form_key = '%s_list_table_form' % (self.get_action_name())
        return session.get(session_table_form_key, {})
    def get_table_sort(self):
        session = self.get_container().get_session()
        session_table_sort_key = '%s_list_table_sort' % (self.get_action_name())
        return session.get(session_table_sort_key, ('id', 'desc'))


class FormAction(BaseAction):
    def __init__(self):
        super(FormAction, self).__init__()
        self.form = None
        self.page_context = None
    def create_form(self):
        pass
    def load_form(self, form):
        pass
    def GET(self):
        self.form = self.create_form()
        self.load_form(self.form)
        self.page_context = self.create_page_context()
        self.page_context.add_widget(self.form)
        return HttpResponse(self.page_context.render())
    def handle_on_success(self, messages):
        self.form = self.create_form()
        for message in messages:
            self.form.add_message(message['type'], message['message'])
        self.load_form(self.form)
        self.page_context = self.create_page_context()
        self.page_context.add_widget(self.form)
        return HttpResponse(self.page_context.render())
    def handle_on_failed(self, messages):
        for message in messages:
            self.form.add_message(message['type'], message['message'])
        self.page_context = self.create_page_context()
        self.page_context.add_widget(self.form)
        return HttpResponse(self.page_context.render())
    def POST(self):
        self.form = self.create_form()
        (status, messages) = self.process_submit(self.form, self.params)
        if status == 'success':
            return self.handle_on_success(messages)
        else:
            return self.handle_on_failed(messages)
    def process_form_data(self, data):
        pass
    def process_submit(self, form, params):
        form.parse_from_params(params)
        data = form.get_form_data()
        result = self.process_form_data(data)
        if result['status'] == 'ok':
            return ('success', [{'type': 'info', 'message': 'The record has been created successfully!'}])
        else:
            for k in result['data']['errors']:
                errors = result['data']['errors'][k]
                form.set_field_errors(k, errors)
            return ('failed', [{'type': 'danger', 'message': 'Error happens'}])


class CreateAction(FormAction):
    pass

class CleanAction(FormAction):
    def process_submit(self, form, params):
        form.parse_from_params(params)
        data = form.get_form_data()
        result = self.process_form_data(data)
        if result['status'] == 'ok':
            process_deleted = result['data']['record']['process_delete']
            return ('success', [{'type': 'info', 'message': '%s process has been cleaned successfully!' % (process_deleted)}])
        else:
            return ('failed', [{'type': 'danger', 'message': 'Error happens'}])

class UpdateAction(FormAction):
    pass

class DeleteAction(BaseAction):
    def GET(self):
        return HttpResponseRedirect('/user/list')
