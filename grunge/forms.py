from django import forms
from .models import Playlist,Track


class CreatePlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name','track','track_sequence']
    track_sequence= forms.IntegerField(initial=1)
    track = forms.ModelMultipleChoiceField(
        queryset=Track.objects.all(),
        widget=forms.Select(choices=Track.objects.all())
    )

class PlayListForm(forms.ModelForm):
   class Meta:
      model=Playlist
      fields=['name']