from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^(?P<topic>[-\w]+)/(?P<slug>[-\w]+)/$',
		view	= 'presentations.views.detail',
		name	= 'presentation_detail',
	),
	url(r'^$',
		view	= 'presentations.views.list',
		name	= 'presentation_list',
	),
)