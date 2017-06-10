from django import forms

class MatchSearch(forms.Form):
    match_search = forms.CharField(label="Enter an word or artist to search for it", max_length=50)

# class ArtistSearch(forms.Form):
#     artist_search = forms.CharField(label="Enter an artist to see their matching lyrics", max_length=50)
