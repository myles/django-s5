from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from presentations.models import *

class PresentationSitemap(Sitemap):
	changefreq = "monthly"
	priority = 0.1
	
	def item(self):
		return Presentation.objects.all()
	
	def lastmod(self, obj):
		return obj.presentation_date
