from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from .views import ItemListView, ItemDetailView, ItemUpdateView, ItemCreateView, ItemDeleteView

urlpatterns = patterns('',
    url(r'^$', ItemListView.as_view(), name='items_list'),
    url(r'^(?P<pk>\d+)/$', ItemDetailView.as_view(), name='item_detail'),
    url(r'^(?P<pk>\d+)/update/$', ItemUpdateView.as_view(), name='item_update'),
    url(r'^(?P<pk>\d+)/delete/$', ItemDeleteView.as_view(), name='item_delete'),
    url(r'^create/$', ItemCreateView.as_view(), name='item_create'),
)