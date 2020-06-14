from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from notasquare.urad_web.renderers import BaseRenderer
from django.template import loader
from . import components

class List(actions.crud.ListAction):
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html  = '<div class="btn-group btn-group">'
            html += '<a class="btn btn-xs btn-success" href="/command/invoke/%s">Invoke</a>' % (row['id'])
            html += '<a class="btn btn-xs btn-primary" href="/command/update/%s">Edit</a>' % (row['id'])
            html += '<a class="btn btn-xs btn-danger" href="/command/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['id'])
            html += '</div>'
            return html
        def render_cell_name(self, table, row):
            return "%s<br/><i style='color: #999'>%s</i>" % (row['name'], row['namespace'])
        def render_cell_command(self, table, row):
            return "%s<br/><i style='color: #999'>%s %s</i>" % (row['docker_image'], row['exec_command'], row['exec_args'])
        def render_cell_resources(self, table, row):
            return "CPU: %sm / %sm <br/>MEM: %sMb / %sMb <br/>Timeout: %s" % (row['cpu_request'], row['cpu_limit'], row['mem_request'], row['mem_limit'], row['timeout'])
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Command')
        table.set_subtitle('List of commands')
        table.create_button('create', '/command/create', 'zmdi-plus')
        table.create_column('id', 'ID', '6%', sortable=True)
        table.create_column('name', 'Name', '20%')
        table.create_column('command', 'Command', '45%')
        table.create_column('resources', 'Resources', '15%')
        table.create_column('actions', '', '14%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=8)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        return components.CommandStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number)

class Create(actions.crud.CreateAction):
    def create_form(self):
        print 'create form'
        form = widgets.form.Form()
        form.set_title('Command')
        form.add_field(widgets.field.Textbox('name'))
        form.add_field(widgets.field.Textbox('namespace'))
        form.add_field(widgets.field.Textbox('docker_image'))
        form.add_field(widgets.field.Textbox('exec_command'))
        form.add_field(widgets.field.Textbox('exec_args'))
        form.add_field(widgets.field.Textbox('cpu_request'))
        form.add_field(widgets.field.Textbox('cpu_limit'))
        form.add_field(widgets.field.Textbox('mem_request'))
        form.add_field(widgets.field.Textbox('mem_limit'))
        form.add_field(widgets.field.Textbox('timeout'))
        form.add_field(widgets.field.List('variables', {
            'name':      widgets.field.Textbox('name'),
            'value':     widgets.field.Textbox('value'),
        }))

        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Command')
        form.renderer.add_field('name', 'Name')
        form.renderer.add_field('namespace', 'Namespace')
        form.renderer.add_field('docker_image', 'Docker Image')
        form.renderer.add_field('exec_command', 'Exec command')
        form.renderer.add_field('exec_args', 'Exec args')
        form.renderer.add_field('cpu_request', 'CPU request')
        form.renderer.add_field('cpu_limit', 'CPU limit')
        form.renderer.add_field('mem_request', 'Memory request')
        form.renderer.add_field('mem_limit', 'Memory limit')
        form.renderer.add_field('timeout', 'Timeout')
        form.renderer.add_field('variables', 'Variables', columns=[
            {'id': 'name',        'label': 'Name',       'width': '35%'},
            {'id': 'value',       'label': 'Value',      'width': '55%'},
        ])

        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form
    def load_form(self, form):
        form.set_form_data({
            'cpu_request': 25,
            'cpu_limit': 200,
            'mem_request': 25,
            'mem_limit': 400,
            'timeout': 0
        })
    def process_form_data(self, data):
        res = components.CommandStore(self.get_container()).create(data)
        return res


class Update(actions.crud.UpdateAction):
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Command')
        form.add_field(widgets.field.Textbox('name'))
        form.add_field(widgets.field.Textbox('namespace'))
        form.add_field(widgets.field.Textbox('docker_image'))
        form.add_field(widgets.field.Textbox('exec_command'))
        form.add_field(widgets.field.Textbox('exec_args'))
        form.add_field(widgets.field.Textbox('cpu_request'))
        form.add_field(widgets.field.Textbox('cpu_limit'))
        form.add_field(widgets.field.Textbox('mem_request'))
        form.add_field(widgets.field.Textbox('mem_limit'))
        form.add_field(widgets.field.Textbox('timeout'))
        form.add_field(widgets.field.List('variables', {
            'name':      widgets.field.Textbox('name'),
            'value':     widgets.field.Textbox('value'),
        }))

        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Command')
        form.renderer.add_field('name', 'Name')
        form.renderer.add_field('namespace', 'Namespace')
        form.renderer.add_field('docker_image', 'Docker Image')
        form.renderer.add_field('exec_command', 'Exec command')
        form.renderer.add_field('exec_args', 'Exec args')
        form.renderer.add_field('cpu_request', 'CPU request')
        form.renderer.add_field('cpu_limit', 'CPU limit')
        form.renderer.add_field('mem_request', 'Memory request')
        form.renderer.add_field('mem_limit', 'Memory limit')
        form.renderer.add_field('timeout', 'Timeout')
        form.renderer.add_field('variables', 'Variables', columns=[
            {'id': 'name',        'label': 'Name',       'width': '35%'},
            {'id': 'value',       'label': 'Value',      'width': '55%'},
        ])

        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form

    def load_form(self, form):
        result = components.CommandStore(self.get_container()).get(self.params['id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        return components.CommandStore(self.get_container()).update(data, self.params['id'])


class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.CommandStore(self.get_container()).delete(self.params['id'])
        return HttpResponseRedirect('/command/list')

class Invoke(actions.BaseAction):
    def GET(self):
        result = components.CommandStore(self.get_container()).invoke(self.params['id'])
        print 'result: %s' %(result)
        return HttpResponseRedirect('/process/view/%s' % (result['data']['pk']))

class Duplicate(Create):
    def load_form(self, form):
        result = components.CommandStore(self.get_container()).get(self.params['id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        res = components.CommandStore(self.get_container()).create(data)
        return res