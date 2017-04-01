from django.conf.urls import url

from . import views
from urllib.parse import quote
from urllib.request import urlretrieve

urlpatterns = [
            # /hhwlookup
            url(r'^$', views.IndexView.as_view(), name='index'),
            # /match/ngram
            url(r'^match/(?P<slug>[\w-]+)/$', views.MatchView.as_view(), name='match_page'),
            # /artist/artistname
            url(r'^artist/(?P<artist>.+)/$', views.ArtistView.as_view(), name='artist_page') ]
