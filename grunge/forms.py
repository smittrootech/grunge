from django import forms
from .models import Playlist,Track,SequenceTrack
from django.forms import formset_factory
from django.forms import modelformset_factory


class CreatePlaylistForm(forms.ModelForm):
    
    track_sequence= forms.IntegerField(initial=1)
    track = forms.ChoiceField(choices=[ (i.id,i.name) for i in Track.objects.all()])
    
    class Meta:
        model = Playlist
        fields = ['name','track_sequence']

    def clean(self):
 
        name = self.cleaned_data.get('name')
        track = self.cleaned_data.get('track')
        track_sequence = self.cleaned_data.get('track_sequence')
        playlist_data, created =Playlist.objects.get_or_create(name=name)
        playlist_id=Playlist.objects.get(name=name).id

        track_name=Track.objects.get(id=track).id
        check_same_track_exist=Playlist.objects.filter(id=playlist_id,tracks__id=track_name)
        if check_same_track_exist:
            err = "already have this track in this playlist"
            self.add_error("track", err)
        check_same_sequence_exist=SequenceTrack.objects.filter(playlist_id=playlist_id,track_sequence=track_sequence)
        if check_same_sequence_exist:
            err = "already have duplicate sequence"
            self.add_error("track_sequence", err)


PlaylistCreateForm = formset_factory(CreatePlaylistForm)

class PlayListForm(forms.ModelForm):
   class Meta:
      model=Playlist
      fields=['name']