from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.conf import settings

from .models import Match
from .models import Song
from .models import Artist 

from .forms import MatchSearch 

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

from itertools import chain

from django.db.models import F

class IndexView(generic.ListView):
    template_name = 'hhlookup/index.html'
    context_object_name = 'match_list'
    
    def get_context_data(self, **kwargs):
        context= super(IndexView, self).get_context_data(**kwargs)
        # Flag to see if we should switch to artist view
        # I'm thinking it looks better with the Artist names always there
        context['artist_view'] = True # artist_form.is_valid()
        print(context['artist_view'])
        return context        

    def get_queryset(self):
            match_form = MatchSearch(self.request.GET)
            print('MATCH FORM', dir(match_form))
            # Are we looking for an ngram?
            if match_form.is_valid() and 'word_search' in self.request.GET:
                return Match.objects.filter(ngram__icontains=match_form.cleaned_data['match_search'])
            # Are we looking for an artist?
            elif match_form.is_valid() and 'artist_search' in self.request.GET:
                return Match.objects.all().filter(found_in_artist__name__icontains=match_form.cleaned_data['match_search'])
            return Match.objects.order_by('?')[:20]
    
class AboutView(generic.TemplateView):
    template_name = 'hhlookup/about.html'
    
class MatchView(generic.ListView):
    model = Match
    template_name = 'hhlookup/match.html'
    context_object_name = 'song_list'

    def get_context_data(self, **kwargs):
        context= super(MatchView, self).get_context_data(**kwargs)
        print('==============>', Match.objects.get(slug=self.kwargs['slug']).ngram)
        context['ngram'] = Match.objects.get(slug=self.kwargs['slug']).ngram
        context['rand'] =  Match.objects.order_by('?').first().slug
        print('RAND', context['rand'])
        return context        

    def get_queryset(self):
        # Dead simple view counter
        match = Match.objects.get(slug=self.kwargs['slug'])
        match.views = F('views') + 1
        match.save()
        print('Match is {}'.format(match))

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
    model = Artist 
    template_name = 'hhlookup/artist.html'
    context_object_name = 'match_list'

    def get_context_data(self, **kwargs):
        print('KWARGS---->', **kwargs)
        context= super(ArtistView, self).get_context_data(**kwargs)
        context['artist'] = Artist.objects.filter(slug=self.kwargs['slug']).name
        context['rand'] =  Artist.objects.order_by('?').first().slug
        print('RAND', context['rand'])
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
        

        matches = Match.objects.all().filter(found_in_artist__slug__contains=self.kwargs['slug'])
        songs_by_match = {m.found_in.all() for m in matches} #Set comprehension to filter identical matches
        # Songs should be a list of querysets [[song1_match1, song2_match1],[song1_match2, song2_match2]]
        if songs_by_match:
            for songs in songs_by_match:
                if songs.exists():
                    for song in songs:
                        song.youtube = gen_youtube_link(song.song_name + ' ' + song.artist)
            return songs_by_match


###############
# API views
###############


# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.renderers import JSONRenderer
# #from rest_framework.parsers import JSONParser
# from hhlookup.serializers import SongSerializer
# 
# @csrf_exempt
# def song_list(request):
#     """
#     List all artists
#     """
#     if request.method == 'GET':
#         songs = Song.objects.all()[:14]
#         print('------------------', songs, '-------------')
#         serializer = SongSerializer(songs, context={'fields':['id', 'song_name']}, many=True)
#         return JsonResponse(serializer.data, safe=False)
# 
#     else:
#         return JsonResponse(serializer.errors, status=405)
#     
# def song_detail(request, pk):
#     """
#     Return artist by alpha name order
#     """
#     try:
#         song = Song.objects.get(pk=pk)     
#     except Song.DoesNotExist:
#         return HttpResponse(status=404)
# 
# 
#     if request.method == 'GET':
#         serializer = SongSerializer(song)
#         return JsonResponse(serializer.data)
#     
#     else:
#         return JsonResponse(serializer.errors, status=405)
#     
