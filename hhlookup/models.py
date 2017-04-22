from django.db import models


class Song(models.Model):
    artist = models.TextField()
    song_name = models.TextField()
    lyrics = models.TextField()
    filename = models.TextField() # This can be used as a unique ID
    old_index = models.IntegerField(default=-1) #This is used to associate it with the match:w
    slug = models.TextField(default="")
    def __str__(self):
        return self.song_name + ' By: ' +  self.artist

class Match(models.Model):
    ngram = models.TextField()
    views = models.IntegerField(default=0) # Count the match views here, to help pick out intersting ones
    flags = models.IntegerField(default=0) # Eventually it would be great to let people flag interesting matches
    found_in = models.ManyToManyField(Song)
    slug = models.TextField(default="")

    def __str__(self):
        return self.ngram
