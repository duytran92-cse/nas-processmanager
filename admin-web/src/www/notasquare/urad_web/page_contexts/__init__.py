
class AbstractPageContext(object):
    pass

class BasePageContext(AbstractPageContext):
    def render(self):
        return self.renderer.render(self)

import standard
