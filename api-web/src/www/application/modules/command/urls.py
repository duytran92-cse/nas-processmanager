
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^get$',       handlers.Get.as_view(),         name='command_get'),
    url(r'^list$',      handlers.List.as_view(),        name='command_list'),
    url(r'^create$',    handlers.Create.as_view(),      name='command_create'),
    url(r'^update$',    handlers.Update.as_view(),      name='command_update'),
    url(r'^delete$',    handlers.Delete.as_view(),      name='command_delete'),
    url(r'^invoke$',    handlers.Invoke.as_view(),      name='command_invoke'),
]
