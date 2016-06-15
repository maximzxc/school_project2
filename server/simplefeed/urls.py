from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView, RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '', url(r'^$', RedirectView.as_view(url="/note-list")),
    url(r'', include('apps.core.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ext/', include('django_select2.urls')),
    url('^markdown/', include('django_markdown.urls')),)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
