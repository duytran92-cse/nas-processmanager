
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^get$',       handlers.Get.as_view(),         name='process_get'),
    url(r'^get_log$',   handlers.Log_Process.as_view(),     name='process_get_log'),
    url(r'^stop$',       handlers.Stop_Process.as_view(),     name='process_stop'),
    url(r'^clean_all$',  handlers.Clean_Process.as_view(),     name='process_clean_all'),
    url(r'^list$',      handlers.List.as_view(),        name='process_list'),
]
