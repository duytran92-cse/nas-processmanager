from notasquare.urad_web.page_contexts import standard
from notasquare.urad_web_material import renderers

class FullPageContext(standard.FullPageContext):
    def __init__(self):
        super(FullPageContext, self).__init__()
        self.app_title = 'Process Manager'
        self.page_title = 'Process Manager'
        self.breadcrumb.add_entry('home', 'Dashboard', '/')
        self.menu.create_menu_group('command', 'Command', '/command/list', 'zmdi-format-subject')
        self.menu.create_menu_group('crontab', 'Crontab', '/crontab/list', 'zmdi-format-subject')
        self.menu.create_menu_group('process', 'Process', '/process/list', 'zmdi-format-subject')
        self.renderer = renderers.page_contexts.FullPageContextRenderer()
