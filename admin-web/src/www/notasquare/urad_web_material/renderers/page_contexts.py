from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer

class FullPageContextRenderer(BaseRenderer):
    def __init__(self):
        super(FullPageContextRenderer, self).__init__()
        self.template = 'material/page_contexts/full.html'
    def render(self, full_page_context):
        template = loader.get_template(self.template)
        context = {
            'app_title':      full_page_context.app_title,
            'page_title':     full_page_context.page_title,
            'menu':           full_page_context.menu,
            'submenu':        full_page_context.submenu,
            'breadcrumb':     full_page_context.breadcrumb,
            'subsubmenu':     full_page_context.subsubmenu,
        }

        widget_html = ''
        for widget in full_page_context.widgets:
            widget_html += widget.render()
        context['widget_html'] = widget_html

        return template.render(context)
