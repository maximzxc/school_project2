from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from core.views import *

from core.api import router

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls, namespace='api')),
    url("^login/$", login, name="login"),
    url("^register/$", register, name="register"),
    url(
        r'^note-list/$',
        NoteListView.as_view(),
        name="note-list"
    ),
    url(
        r'^note/(?P<slug>[a-zA-Z-_0-9]+)/$',
        NoteDetailView.as_view(),
        name="note-detail"
    ),
    url(
        r'^note/(?P<slug>.*)/update/$',
        NoteUpdateView.as_view(),
        name="note-update"
    ),

    url(
        r'^note/(?P<slug>[a-zA-Z-_0-9]+)/delete/$',
        NoteDeleteView.as_view(),
        name="note-delete"
    ),

    url(
        r'^note-create/$',
        NoteCreateView.as_view(),
        name="note-create"
    ),
)
