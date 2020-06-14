from notasquare.urad_web.containers.standard import Container as StandardContainer
from . import page_contexts

class Container(StandardContainer):
    def get_default_page_context(self):
        return page_contexts.FullPageContext()
