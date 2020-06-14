
class AbstractWidget(object):
    pass

class BaseWidget(AbstractWidget):
    def __init__(self):
        super(BaseWidget, self).__init__()
        self.renderer = None
    def set_renderer(self, renderer):
        self.renderer = renderer
    def render(self):
        return self.renderer.render(self)

import table
import field
import form
