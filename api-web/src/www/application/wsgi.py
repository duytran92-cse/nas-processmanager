import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application.settings." + os.environ.get('APP_ENV'))

application = get_wsgi_application()
