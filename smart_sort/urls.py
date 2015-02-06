# url conf for the django app: smart_sort
from django.conf.urls import patterns, url
from smart_sort import views

urlpatterns = patterns('',
    url(r'^$', views.ss_page, name="ss_page"), # UI demo page
    url(r'^api/$', views.ss_api), # the service
)
