
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^$',                          actions.List.as_view(),     name='command_list'),
    url(r'^list$',                      actions.List.as_view(),     name='command_list'),
    url(r'^create$',                    actions.Create.as_view(),   name='command_create'),
    url(r'^create/(?P<id>([0-9]+))$',                    actions.Duplicate.as_view(),   name='command_duplicate'),
    url(r'^delete/(?P<id>([0-9]+))$',   actions.Delete.as_view(),   name='command_delete'),
    url(r'^update/(?P<id>([0-9]+))$',   actions.Update.as_view(),   name='command_update'),
    url(r'^invoke/(?P<id>([0-9]+))$',   actions.Invoke.as_view(),   name='command_invoke'),
]
