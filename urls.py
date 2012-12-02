from django.conf.urls.defaults import *
from views import detail, list
urlpatterns = patterns('',
	url(r'^(?P<topic>[-\w]+)/(?P<slug>[-\w]+)/$',
		view	= detail,
		name	= 'presentation_detail',
	),
	url(r'^$',
		view	= list,
		name	= 'presentation_list',
	),
)
