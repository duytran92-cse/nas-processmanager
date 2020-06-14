from notasquare.urad_web.page_contexts import BasePageContext

class FullPageContext(BasePageContext):
    class Breadcrumb(object):
        def __init__(self):
            self.entries = []
        def build(self):
            self.entries = []
        def add_entry(self, name, title, url = ''):
            self.entries.append({
                'name':   name,
                'title':  title,
                'url':    url
            })
    class Menu(object):
        def __init__(self):
            self.groups = []
            self.group_selected = ''
            self.entry_selected = ''
        class MenuGroup(object):
            def __init__(self, name, title, url, iclass):
                self.name = name
                self.title = title
                self.url = url
                self.iclass = iclass
                self.entries = []
            def add_menu_entry(self, name, title, url):
                self.entries.append({
                    'name':      name,
                    'title':     title,
                    'url':       url
                })
        def build(self):
            pass
        def create_menu_group(self, name, title, url = '', iclass = ''):
            menu_group = self.MenuGroup(name, title, url, iclass)
            self.groups.append(menu_group)
            return menu_group
        def set_group_selected(self, group):
            self.group_selected = group
        def set_entry_selected(self, entry):
            self.entry_selected = entry
    def __init__(self):
        super(FullPageContext, self).__init__()
        self.app_title = ''
        self.page_title = ''
        self.menu = self.Menu()
        self.submenu = self.Menu()
        self.subsubmenu = self.Menu()
        self.breadcrumb = self.Breadcrumb()
        self.widgets = []
        self.renderer = None
    def add_widget(self, widget):
        self.widgets.append(widget)
