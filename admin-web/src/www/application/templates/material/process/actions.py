from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from notasquare.urad_web.renderers import BaseRenderer
from django.template import loader
from django.core import serializers
from . import components

class List(actions.crud.ListAction):
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html = '<div class="btn-group btn-group">'
            html += '<a class="btn btn-xs btn-primary" href="/process/view/%s">View</a>' % (row['id'])

            html += '<a id="btn_stop" class="btn btn-xs btn-danger" value="%s,%s" style="display: none">Stop</a>' % (
            row['status'], row['id'])
            html += '</div>'
            return html
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Process')
        table.set_subtitle('List of process')
        table.create_button('delete', '/process/clean_all','zmdi-close')
        table.create_column('id', 'ID', '6%', sortable=True)
        table.create_column('timestamp', 'Timestamp', '15%')
        table.create_column('command_label', 'Command', '25%')
        table.create_column('status', 'Status', '10%')
        table.create_column('message', 'Message', '30%')
        table.create_column('actions', '', '14%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=8)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        return components.ProcessStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number)

class View(actions.BaseAction):
    class ViewWidget(widgets.BaseWidget):
        class ViewRenderer(BaseRenderer):
            def render(self, view_widget):
                template = loader.get_template('material/process/view.html')
                context = {}
                context['process'] = view_widget.process
                return template.render(context)
        def build(self, params):
            self.process = components.ProcessStore(self.container).get(params['id'])['data']['record']
            self.renderer = self.ViewRenderer()
    def create_process_widget(self, params):
        widget = self.ViewWidget()
        widget.container = self.get_container()
        widget.build(params)
        return widget
    def GET(self):
        self.page_context = self.create_page_context()
        self.page_context.add_widget(self.create_process_widget(self.params))
        return HttpResponse(self.page_context.render())

class Log_Process(actions.BaseAction):
    def GET(self):
        log = components.ProcessStore(self.container).get_log(self.params['id'])['data']['record']
        print log
        return HttpResponse(log)

class Stop_Process(actions.BaseAction):
    def GET(self):
        response = components.ProcessStore(self.container).stop(self.params['id'])['data']['record']
        print response
        return HttpResponse(response)

class CreateProcessClean(actions.crud.CleanAction):
    def create_page_context(self):
        return components.ProcessFullPageContext(self.params, self.container)

    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Clean all Processs')
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Clean all Proecsss with status not is Running')
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('multiple_choice', renderers.widgets.field.MultipleChoiceRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form

    def load_form(self, form):
        form.set_form_data({
        })

    def process_form_data(self):
        response = components.ProcessStore(self.get_container()).clean_all({})
        print response
        return response