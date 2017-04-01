from django import forms

class MatchSearch(forms.Form):
    match_search = forms.CharField(label="Enter a word or two to find a phrase that contains it", max_length=50)
