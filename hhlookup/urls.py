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
            url(r'^artist/(?P<slug>[\w-]+)/$', views.ArtistView.as_view(), name='artist_page'), 
########
# API urls
######
#             url(r'^api/v1/$', views.song_list),
#             url(r'^api/v1/(?P<pk>[0-9]+)/$', views.song_detail),
#             ]

