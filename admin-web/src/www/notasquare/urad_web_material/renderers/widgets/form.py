from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer

class HorizontalFormRenderer(BaseRenderer):
    def __init__(self):
        super(HorizontalFormRenderer, self).__init__()
        self.template = 'material/widgets/form/horizontal.html'
        self.field_renderers = {}
        self.rows = []
        self.form_id = 'MainForm'
    def add_section(self, label):
        self.rows.append({'type': 'section', 'label': label})
    def add_field(self, id, label, **kwargs):
        self.rows.append({'type': 'field', 'id': id, 'label': label, 'options': kwargs})
    def render_section(self, label):
        field_html = '<h4 style="font-size: 15px">' + str(label) + '</h4>'
        return ('<div class="row form-group"><div class="col-sm-12">%s</div></div>' % (field_html))
    def render_field(self, label, field, options):
        field.label = label
        field_html = self.field_renderers[field.code].render(field, options)
        return ('<div class="row form-group"><div class="col-sm-12">%s</div></div>' % (field_html))
    def set_field_renderer(self, code, renderer):
        self.field_renderers[code] = renderer
    def build_context(self, form, context):
        context['form_id'] = self.form_id
        context['title'] = form.title
        context['messages'] = form.messages
        context['tabs'] = form.tabs
        context['active_tab'] = form.active_tab
        context['buttons'] = form.buttons
        form_html = ''
        for row in self.rows:
            if row['type'] == 'section':
                form_html += self.render_section(row['label'])
            else:
                field = form.fields[row['id']]
                form_html += self.render_field(row['label'], field, row['options'])
        context['form_html'] = form_html
    def render(self, form):
        template = loader.get_template(self.template)
        context = {}
        self.build_context(form, context)
        return template.render(context)

class TableFormRenderer(BaseRenderer):
    def __init__(self):
        super(TableFormRenderer, self).__init__()
        self.template = 'material/widgets/table_form/4_columns.html'
        self.field_renderers = {}
        self.rows = []
        self.form_id = 'TableForm'
    def add_field(self, id, label, **kwargs):
        self.rows.append({'type': 'field', 'id': id, 'label': label, 'options': kwargs})
    def set_field_renderer(self, code, renderer):
        self.field_renderers[code] = renderer
    def render_field(self, label, field, options):
        field.label = label
        field_html = self.field_renderers[field.code].render(field, options)
        colspan = options['colspan'] if 'colspan' in options else 3
        return ('<div class="col-sm-' + str(colspan) + '"><div class="form-group">%s</div></div>' % (field_html))
    def render(self, table):
        template = loader.get_template(self.template)
        context = {}
        context['form_id'] = self.form_id
        context['messages'] = table.messages

        form_html = ''
        for row in self.rows:
            field = table.fields[row['id']]
            form_html += self.render_field(row['label'], field, row['options'])

        context['form_html'] = form_html
        return template.render(context)
