from rest_framework import serializers
from hhlookup.models import Song

class SongSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(SongSerializer, self).__init__(*args, **kwargs)

        if 'fields' in self.context:
            # Get the "fields" to include
            fields = self.context['fields']
            chosen = set(fields)
            all_fields = set(self.fields.keys())
            # Pop anything not in the supplied list of fields and asign them as the fields
            for field in all_fields - chosen:
                self.fields.pop(field)
            
        # If fields are not specified, return all

    class Meta:
        model = Song
        fields = ('id', 'artist', 'song_name', 'lyrics')

