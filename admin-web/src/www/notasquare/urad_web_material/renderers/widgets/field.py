from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer


class FieldRenderer(BaseRenderer):
    def __init__(self):
        self.template = 'material/widgets/field/field.html'
    def render(self, field, options):
        template = loader.get_template(self.template)
        context = {}
        context['field'] = field
        context['options'] = options
        return template.render(context)


class TextboxRenderer(FieldRenderer):
    def __init__(self):
        super(TextboxRenderer, self).__init__()
        self.template = 'material/widgets/field/textbox.html'


class TextareaRenderer(FieldRenderer):
    def __init__(self):
        super(TextareaRenderer, self).__init__()
        self.template = 'material/widgets/field/textarea.html'

class RichtextRenderer(FieldRenderer):
    def __init__(self):
        super(RichtextRenderer, self).__init__()
        self.template = 'material/widgets/field/richtext.html'

class ComboboxRenderer(FieldRenderer):
    def __init__(self):
        super(ComboboxRenderer, self).__init__()
        self.template = 'material/widgets/field/combobox.html'


class MultipleChoiceRenderer(FieldRenderer):
    def __init__(self):
        super(MultipleChoiceRenderer, self).__init__()
        self.template = 'material/widgets/field/multiple_choice.html'


class CollectionRenderer(FieldRenderer):
    def __init__(self):
        super(CollectionRenderer, self).__init__()
        self.template = 'material/widgets/field/collection.html'
        self.field_renderers = {}
        self.field_renderers['textbox']  = TextboxRenderer()
        self.field_renderers['textarea'] = TextareaRenderer()
        self.field_renderers['combobox'] = ComboboxRenderer()
    def render_row(self, row):
        return '----'
    def render(self, field):
        template = loader.get_template(self.template)
        context = {}
        context['field'] = field
        row_htmls = []
        for row in field.data:
            row_htmls.append(self.render_row(row))
        context['row_htmls'] = row_htmls
        return template.render(context)


class ListRenderer(FieldRenderer):
    def __init__(self):
        super(ListRenderer, self).__init__()
        self.template = 'material/widgets/field/list.html'
        self.field_renderers = {}
        self.field_renderers['textbox'] = TextboxRenderer()
        self.field_renderers['textarea'] = TextareaRenderer()
        self.field_renderers['combobox'] = ComboboxRenderer()
    def render_row(self, list, row, columns, row_index):
        html = ''
        html += '<tr row-index="' + str(row_index) + '">'
        for column in columns:
            field = list.fields[column['id']]
            data = row[column['id']] if column['id'] in row else ''
            field.set_data(data)
            field.id = column['id'] + '_' + str(row_index)
            html += '<td>'
            html += self.field_renderers[field.code].render(field, {})
            html += '</td>'
        html += '<td style="vertical-align: bottom">'
        html += '    <div class="btn-group pull-right">'
        html += '        <a id="%s_insert" href="javascript:field_list_insert(\'%s\', \'%s\')" class="btn btn-xs btn-primary">Insert</a>' % (column['id'], list.id, str(row_index))
        html += '        <a id="%s_remove" href="javascript:field_list_remove(\'%s\', \'%s\')" class="btn btn-xs btn-danger">Remove</a>' % (column['id'], list.id, str(row_index))
        html += '    </div>'
        html += '</td>'
        html += '</tr>'
        return html
    def render(self, list, options):
        template = loader.get_template(self.template)
        context = {}

        columns = []
        if 'columns' in options:
            columns = options['columns']
        else:
            columns = []
        context['columns'] = columns

        context['field'] = list
        row_htmls = ''
        row_index = 1
        for row in list.data:
            row_htmls += self.render_row(list, row, columns, row_index)
            row_index += 1
        context['row_htmls'] = row_htmls

        context['current_row_index'] = row_index

        context['row_html_prototype'] = self.render_row(list, {}, columns, '__ROW_INDEX__')
        return template.render(context)
