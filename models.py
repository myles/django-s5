from django.db.models import permalink
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from basic.places.models import Place
import os


def get_theme_path():
    if settings.DEBUG == True:
        app_root = os.path.dirname(os.path.abspath(__file__))
        static_dir = os.path.join(app_root, 'static/s5/')
    else:
        static_dir = os.path.join(settings.STATIC_ROOT, 's5/')
        print static_dir
    return static_dir


class Topic(models.Model):
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)

    class Meta:
        verbose_name = _('topic')
        verbose_name_plural = _('topics')

    def __unicode__(self):
        return u"%s" % self.title

    @property
    def presentation_count(self):
        return u"%s" % self.presentation_set.all().count()

    @permalink
    def get_absolute_url(self):
            return ('topic_detail', None, {
                            'slug': self.slug,
                            })


class Presentation(models.Model):
    DEFAULT_VIEW_CHOICE = (
        ('slideshow', 'Slideshow'),
        ('outline', 'Outline')
        )

    CONTROL_VIS_CHOICE = (
        ('visible', 'Visible'),
        ('hidden', 'Hidden')
        )
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    topic = models.ForeignKey(Topic)
    author = models.ForeignKey(User, blank=True, null=True)
    presentation_date = models.DateField(_('presentation date'))
    company = models.CharField(
        _('company'),
        blank=True,
        null=True,
        max_length=200
        )
    company_url = models.URLField(
        _('company_url'),
        blank=True,
        verify_exists=True
        )
    place = models.ForeignKey(Place, blank=True, null=True)
    default_view = models.CharField(
        _('default view'),
        choices=DEFAULT_VIEW_CHOICE,
        default="slideshow",
        max_length=9
        )
    control_vis = models.CharField(
        _('controls visible'),
        choices=CONTROL_VIS_CHOICE, default="hidden", max_length=7)
    theme = models.FilePathField(
        match="slides.css",
        path=get_theme_path(), recursive=True)
    header = models.TextField(
        _('header'), blank=True, null=True, help_text="Use raw HTML.")
    footer = models.TextField(
        _('footer'), blank=True, null=True, help_text="Use raw HTML.")
    topleft = models.TextField(
        _('top left'), blank=True, null=True, help_text="Use raw HTML.")
    topright = models.TextField(
        _('top right'), blank=True, null=True, help_text="Use raw HTML.")
    bottomleft = models.TextField(
        _('bottom left'), blank=True, null=True, help_text="Use raw HTML.")
    bottomright = models.TextField(
        _('bottom right'),
        blank=True, null=True, help_text="Use raw HTML.")

    class Meta:
        verbose_name = _('presentation')
        verbose_name_plural = _('presentations')
        ordering = ('-presentation_date',)

    def __unicode__(self):
        return u"%s" % self.title

    @permalink
    def get_absolute_url(self):
        return ('presentation_detail', None, {
                'slug': self.slug,
                'topic': self.topic.slug,
                })

    @property
    def get_theme_url(self):
        return self.theme.split('/s5/')[-1]

    def get_next_slide_weight(presentation):
        try:
            last = Slide.objects.order_by('-id').filter(
                presentation=presentation
                )[0]
        except IndexError:
            return '1'

        return str(int(last.weight) + 1)


class Slide(models.Model):
    presentation = models.ForeignKey(Presentation)
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('slide content'), help_text="Use Textile.")
    handout = models.TextField(
        _('slide handout'), help_text="Ues Textile.", blank=True, null=True)
    weight = models.IntegerField(_('weight'), editable=False)

    class Meta:
        verbose_name = _('slide')
        verbose_name_plural = _('slides')
        ordering = ('presentation', 'weight')

        # class Admin:
        #         list_display	= ('title', 'presentation')
        #         list_filter		= ('presentation',)
        #         ordering		= ('presentation', 'weight')

    def save(self):
        self.weight = Presentation.get_next_slide_weight(self.presentation)
        super(Slide, self).save()

    def __unicode__(self):
        return u"%s" % self.title

    def get_absolute_url(self):
        return self.presentation.get_absolute_url()
