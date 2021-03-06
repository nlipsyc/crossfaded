from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.conf import settings

from .models import Match
from .models import Song

from .forms import MatchSearch

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

class IndexView(generic.ListView):
    template_name = 'hhlookup/index.html'
    context_object_name = 'match_list'

    

    def get_queryset(self):
            form = MatchSearch(self.request.GET)
            print('FFFFFFFFF', dir(form))
            if form.is_valid() and form.cleaned_data['match_search']:
                return Match.objects.filter(ngram__icontains=form.cleaned_data['match_search'])
            return Match.objects.order_by('?')[:20]
    

class MatchView(generic.ListView):
    model = Match
    template_name = 'hhlookup/match.html'
    context_object_name = 'song_list'

    def get_context_data(self, **kwargs):
        context= super(MatchView, self).get_context_data(**kwargs)
        print('==============>', Match.objects.get(slug=self.kwargs['slug']).ngram)
        context['ngram'] = Match.objects.get(slug=self.kwargs['slug']).ngram
        return context        

    def get_queryset(self):

        def gen_youtube_link(query):
            youtube = build(settings.YOUTUBE_API_SERVICE_NAME, settings.YOUTUBE_API_VERSION,
    developerKey=settings.YOUTUBE_DEVELOPER_KEY)
            resp = youtube.search().list(q=query, part="id", maxResults=15).execute()
            
            if resp['items']:
                filt_resp = [i for i in resp['items'] if i['id']['kind'] == 'youtube#video']
                print('+++++++++++', filt_resp[0]['id']['videoId'])
                return "https://www.youtube.com/embed/" + filt_resp[0]['id']['videoId']

            else:
                return "https://www.youtube.com/embed/" + 'innelegantStubForMissingVideo'


        print('---------------->', self.kwargs)
        songs =  Match.objects.get(slug=self.kwargs['slug']).found_in.all()
        for song in songs:
            song.youtube = gen_youtube_link(song.song_name + ' ' + song.artist)
        return songs

class ArtistView(generic.DetailView):
    model = Match
    template_name = 'hhlookup/match.html'
def artist_page(request, artist):
    return HttpResponse("You're looking at the matches for %s." % artist)

