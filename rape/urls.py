try:
	from django.conf.urls import url, patterns
except:
	from django.conf.urls.defaults import *

urlpatterns = patterns('rape.views',
	url(r'^script/([0-9]+)/([a-z0-9]+).js$', 'resource', {"res_type":'script'}, name='raped_script'),
	url(r'^style/([0-9]+)/([a-z0-9]+).css$', 'resource', {"res_type":'style'},  name='raped_style'),
)
