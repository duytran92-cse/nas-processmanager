from django.conf.urls import include, url

urlpatterns = [
    url(r'^',                               include('application.modules.command.urls')),
    url(r'^command/',                       include('application.modules.command.urls')),
    url(r'^crontab/',                       include('application.modules.crontab.urls')),
    url(r'^process/',                       include('application.modules.process.urls')),
]
