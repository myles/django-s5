Django S5
=========
- [GitHub](http://github.com/myles/django-basic-tumblelog/)
- [Lighouse](http://myles.lighthouseapp.com/projects/14172)

A [Django](http://djangoproject.com/) reusable application for presentations
powered by [S5](http://meyerweb.com/eric/tools/s5/).

Dependancies
------------
- [Django](http://djangoproject.com/)
- [Django Basic Places](https://github.com/nathanborror/django-basic-apps)
- [Django Tagging](http://code.google.com/p/django-tagging/)
- [S5](http://meyerweb.com/eric/tools/s5/)

Install
-------
1. clone this repository
2. Rename it as you like
3. Added it to your INSTALLED_APPS.
4. add the requirements to your INSTALLED_APPS:

exemple:

    INSTALLED_APPS = (
                  ...
                  'basic.places',
                  'tagging',
                  'django.contrib.markup'
                  ...
    )

5. update your urls.py to link to the app.

If the app is called "presentation":

     url(r'^presentation/', include('presentation.urls')),

1. Run `syncdb`.
