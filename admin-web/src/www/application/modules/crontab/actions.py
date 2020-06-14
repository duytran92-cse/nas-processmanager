from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from notasquare.urad_web.renderers import BaseRenderer
from django.template import loader
from . import components
from application.modules.command import components as command_components

class List(actions.crud.ListAction):
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html  = '<div class="btn-group btn-group">'            
            html += '<a class="btn btn-xs btn-primary" href="/crontab/update/%s">Edit</a>' % (row['id'])
            html += '<a class="btn btn-xs btn-danger" href="/crontab/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['id'])
            html += '</div>'
            return html
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Crontab')
        table.set_subtitle('List of crontab')
        table.create_button('create', '/crontab/create', 'zmdi-plus')
        table.create_column('id', 'ID', '6%', sortable=True)
        table.create_column('month', 'Month', '6%')
        table.create_column('day', 'Day', '6%')
        table.create_column('hour', 'Hour', '6%')
        table.create_column('minute', 'Minute', '6%')
        table.create_column('num_process', 'Num Process', '10%')
        table.create_column('command_label', 'Command', '46%')
        table.create_column('actions', '', '14%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=8)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        return components.CrontabStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number)


class Create(actions.crud.CreateAction):
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Crontab')
        form.add_field(widgets.field.Textbox('month'))
        form.add_field(widgets.field.Textbox('day'))
        form.add_field(widgets.field.Textbox('hour'))
        form.add_field(widgets.field.Textbox('minute'))
        form.add_field(widgets.field.Textbox('num_process'))
        form.add_field(widgets.field.Combobox('command_id', choices=command_components.CommandStore(self.container).populate_combobox()))

        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Crontab')
        form.renderer.add_field('month', 'Month')
        form.renderer.add_field('day', 'Day')
        form.renderer.add_field('hour', 'Hour')
        form.renderer.add_field('minute', 'Minute')
        form.renderer.add_field('num_process', 'Num Process')
        form.renderer.add_field('command_id', 'Command')

        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form
    def load_form(self, form):
        form.set_form_data({
        })
    def process_form_data(self, data):
        res = components.CrontabStore(self.get_container()).create(data)
        return res


class Update(actions.crud.UpdateAction):
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Crontab')
        form.add_field(widgets.field.Textbox('month'))
        form.add_field(widgets.field.Textbox('day'))
        form.add_field(widgets.field.Textbox('hour'))
        form.add_field(widgets.field.Textbox('minute'))
        form.add_field(widgets.field.Textbox('num_process'))
        form.add_field(widgets.field.Combobox('command_id', choices=command_components.CommandStore(self.container).populate_combobox()))

        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Crontab')
        form.renderer.add_field('month', 'Month')
        form.renderer.add_field('day', 'Day')
        form.renderer.add_field('hour', 'Hour')
        form.renderer.add_field('minute', 'Minute')
        form.renderer.add_field('num_process', 'Num Process')
        form.renderer.add_field('command_id', 'Command')

        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form

    def load_form(self, form):
        result = components.CrontabStore(self.get_container()).get(self.params['id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        return components.CrontabStore(self.get_container()).update(data, self.params['id'])


class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.CrontabStore(self.get_container()).delete(self.params['id'])
        return HttpResponseRedirect('/crontab/list')
