# url conf for the django app: csv_analyzer
from django.conf.urls import patterns, url
from csv_analyzer import views

urlpatterns = patterns('',
    url(r'^$', views.select_file, name="home"), # choose csv file to analyze
    url(r'^analyze/(?P<filename>\S+)/?$', views.analyze, name="analyze"), # display results
)
