from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer


class TableRenderer(BaseRenderer):
    def __init__(self):
        super(TableRenderer, self).__init__()
        self.template = 'material/widgets/table/table.html'
    def render_row(self, table, row):
        row_html = '<tr>'
        for column in table.columns:
            method = 'render_cell_' + str(column.name)
            if hasattr(self, method):
                f = getattr(self, method)
                row_html += '<td>' + f(table, row) + '</td>'
            else:
                row_html += '<td>' + (str(row[column.name]) if column.name in row else '') + '</td>'
        row_html += '</tr>'
        return row_html
    def render(self, table):
        template = loader.get_template(self.template)
        context = {}
        context['title'] = table.title
        context['subtitle'] = table.subtitle
        context['columns'] = table.columns
        context['buttons'] = table.buttons
        rows_html = ''
        for row in table.data:
            rows_html += self.render_row(table, row)
        context['rows_html'] = rows_html
        return template.render(context)


class DataTableRenderer(BaseRenderer):
    def __init__(self):
        super(DataTableRenderer, self).__init__()
        self.template = 'material/widgets/table/data_table.html'
        self.table_form_renderer = None
    def render_row(self, table, row):
        row_html = '<tr>'
        for column in table.columns:
            method = 'render_cell_' + str(column.name)

            if hasattr(self, method):
                f = getattr(self, method)
                if column.name == 'name':
                    id =  row['id']
                    print column.name
                    row_html += '<td style="position: relative;">' + f(table, row) + \
                                '<a class ="btn btn-xs btn-primary" style="top:12%; right:5%; position: absolute;" href="/command/create/'+ str(id) +'" > Duplicate </a>' + '</td>'
                else:
                    row_html += '<td>' + f(table, row) + '</td>'

            else:
                if row.has_key('name'):
                    row_html += '<td>' + (str(row[column.name]) if column.name in row else '') + '</td>'
                else:
                    row_html += '<td>' + (str(row[column.name]) if column.name in row else '') + '</td>'

        row_html += '</tr>'
        return row_html
    def render(self, table):
        template = loader.get_template(self.template)
        context = {}
        context['title'] = table.title
        context['subtitle'] = table.subtitle
        context['columns'] = table.columns
        context['buttons'] = table.buttons
        rows_html = ''
        for row in table.data:
            rows_html += self.render_row(table, row)
        context['rows_html'] = rows_html

        # Pagination
        start_index = max(1, table.current_page - 2)
        end_index = min(table.total_pages, table.current_page + 2 ) + 1
        context['pages_range'] = range(start_index, end_index)
        context['current_page'] = table.current_page
        context['previous_page_i'] = table.current_page - 1
        context['next_page_i'] = table.current_page + 1
        context['total_pages'] = table.total_pages
        context['total_records'] = table.total_records
        context['start_record_index'] = (table.current_page - 1)* table.record_per_page + 1
        context['end_record_index'] = min((table.current_page * table.record_per_page), table.total_records)

        # Filter form
        if self.table_form_renderer != None:
            context['table_form_html'] = self.table_form_renderer.render(table)

        return template.render(context)
