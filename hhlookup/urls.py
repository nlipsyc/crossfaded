from django.conf.urls import url

from . import views
from urllib.parse import quote
from urllib.request import urlretrieve

urlpatterns = [
            # /crossfaded
            url(r'^$', views.IndexView.as_view(), name='index'),
            # /crossfaded/about 
            url(r'^about/$', views.AboutView.as_view(), name='about'),
            # /match/ngram
            url(r'^match/(?P<slug>[\w-]+)/$', views.MatchView.as_view(), name='match_page'),
            # /artist/artistname
            url(r'^artist/(?P<artist>.+)/$', views.ArtistView.as_view(), name='artist_page') ]

