
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^$',                          actions.List.as_view(),     name='process_list'),
    url(r'^list$',                      actions.List.as_view(),     name='process_list'),
    url(r'^view/(?P<id>([0-9]+))$',     actions.View.as_view(),     name='process_view'),
    url(r'^stop/(?P<id>([0-9]+))$',     actions.Stop_Process.as_view(),     name='process_stop'),
    url(r'^clean_all$',                 actions.CreateProcessClean.as_view(),     name='process_clean_all'),
    url(r'^view/(?P<id>([0-9]+))/stream_log$',     actions.Log_Process.as_view(),     name='process_stream_log'),
]
