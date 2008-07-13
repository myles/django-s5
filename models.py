from django.db.models import permalink
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.conf import settings

class Presentation(models.Model):
	DEFAULT_VIEW_CHOICE = (
		('slideshow', 'Slideshow'),
		('outline', 'Outline')
	)
	CONTROL_VIS_CHOICE = (
		('visible', 'Visible'),
		('hidden', 'Hidden')
	)
	title				= models.CharField(_('title'), max_length=200)
	slug				= models.CharField(_('slug'), max_length=100, prepopulate_from=('title',), unique=True)
	author				= models.ForeignKey(User, blank=True, null=True)
	presentation_date	= models.DateField(_('presentation date'))
	company				= models.CharField(_('company'), blank=True, null=True, max_length=200)
	company_url			= models.URLField(_('company_url'), blank=True, verify_exists=True)
	default_view		= models.CharField(_('default view'), choices=DEFAULT_VIEW_CHOICE, default="slideshow", max_length=9)
	control_vis			= models.CharField(_('controls visible'), choices=CONTROL_VIS_CHOICE, default="hidden", max_length=7)
	theme				= models.FilePathField(match="slides.css", path=settings.MEDIA_ROOT + "/s5", recursive=True)
	header				= models.TextField(_('header'), blank=True, null=True, help_text="Use raw HTML.")
	footer				= models.TextField(_('footer'), blank=True, null=True, help_text="Use raw HTML.")
	topleft				= models.TextField(_('top left'), blank=True, null=True, help_text="Use raw HTML.")
	topright			= models.TextField(_('top right'), blank=True, null=True, help_text="Use raw HTML.")
	bottomleft			= models.TextField(_('bottom left'), blank=True, null=True, help_text="Use raw HTML.")
	bottomright			= models.TextField(_('bottom right'), blank=True, null=True, help_text="Use raw HTML.")
	
	class Meta:
		verbose_name		= _('presentation')
		verbose_name_plural	= _('presentations')
		db_table			= 'presentations'
		ordering			= ('-presentation_date',)
	
	class Admin:
		list_display	= ('title', 'author', 'presentation_date',)
		list_filter		= ('author',)
		ordering		= ('-presentation_date',)
		fields			= (
			(None, {
				'fields': (('title', 'slug'), ('author', 'presentation_date'), 'header', 'footer', ('company', 'company_url'), ('default_view', 'control_vis', 'theme'))
			}),
			('Optional', {
				'classes': 'collapse',
				'fields': ('topleft', 'topright', 'bottomleft', 'bottomright')
			}),
		)
	
	def __unicode__(self):
		return u"%s" % self.title
	
	@permalink
	def get_absolute_url(self):
		return ('presentation_detail', None, {
			'slug'	: self.slug,
		})
	
	@property
	def get_theme_url(self):
		return '/' + str(self.theme).split(settings.MEDIA_ROOT)[-1]

def get_next_slide_weight(presentation):
	try:
		last = Slide.objects.order_by('-id').filter(presentation=presentation)[0]
	except IndexError:
		return '1'
	
	return str(int(last.weight) + 1)

class Slide(models.Model):
	presentation		= models.ForeignKey(Presentation)
	title				= models.CharField(_('title'), max_length=200)
	content				= models.TextField(_('slide content'), help_text="Use Textile.")
	handout				= models.TextField(_('slide handout'), help_text="Ues Textile.", blank=True, null=True)
	weight				= models.IntegerField(_('weight'), editable=False)
	
	class Meta:
		verbose_name		= _('slide')
		verbose_name_plural	= _('slides')
		db_table			= 'presentation_slides'
		ordering			= ('presentation', 'weight')
	
	class Admin:
		list_display	= ('title', 'presentation')
		list_filter		= ('presentation',)
		ordering		= ('presentation', 'weight')
	
	def save(self):
		self.weight = get_next_slide_weight(self.presentation)
		super(Slide, self).save()
	
	def __unicode__(self):
		return u"%s" % self.title
	
	def get_absolute_url(self):
		return self.presentation.get_absolute_url()
