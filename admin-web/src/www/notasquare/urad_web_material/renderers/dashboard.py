from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer

class DashboardRenderer(BaseRenderer):
    def __init__(self):
        super(DashboardRenderer, self).__init__()
        self.template = 'material/dashboard/dashboard.html'
    def render(self, table):
        template = loader.get_template(self.template)
        context = {}
        context['links'] = table.data[0]['links']
        context['records'] = table.data[1]['records']
        return template.render(context)
