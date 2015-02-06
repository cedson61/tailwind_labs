from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),    
    url(r'^about/$', TemplateView.as_view(template_name="about.html"), name='about'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^items/', include('items.urls', namespace='items', app_name='items')),
    url(r'^csv/', include('csv_analyzer.urls', namespace='csv_analyzer', app_name='csv_analyzer')),
    url(r'^sort/', include('smart_sort.urls', namespace='smart_sort', app_name='smart_sort')),
)

urlpatterns += patterns(
    'django.contrib.auth.views',  # common prefix for all the view names to follow

    url(r'^login/$', 'login',
        {'template_name': 'login.html'},
        name='tailwind_labs_login'),
    
    url(r'^logout/$', 'logout',
        {'next_page': 'home'},
        name='tailwind_labs_logout'),
)