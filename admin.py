from django.contrib import admin
from models import Topic, Presentation, Slide


class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class PresentationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display  = ('title', 'author', 'presentation_date', 'topic',)
    list_filter  = ('author',)
    ordering = ('-presentation_date',)
    fieldset = (
        (None, {
                'fields': (
                    ('title', 'slug'),
                    ('author', 'presentation_date'),
                    'header',
                    'footer',
                    ('company', 'company_url'),
                    ('default_view', 'control_vis', 'theme'),
                    ('topic', 'place'))
                }
         ),
        ('Optional', {
                'classes': 'collapse',
                'fields': ('topleft', 'topright', 'bottomleft', 'bottomright')
                }),
        )


class AdminSlide(admin.ModelAdmin):
    pass

admin.site.register(Slide)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Presentation, PresentationAdmin)
