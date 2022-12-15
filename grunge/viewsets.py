from django.http import JsonResponse
from rest_framework import viewsets

from .filters import AlbumFilter, ArtistFilter, TrackFilter
from .models import Album, Artist, Track,Playlist,SequenceTrack
from .serializers import AlbumSerializer, ArtistSerializer, TrackSerializer,PlaylistSerializer
from rest_framework import mixins
from rest_framework.response import Response
import json
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CreatePlaylistForm,PlayListForm,PlaylistCreateForm
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.views import View
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect





class BaseAPIViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"


class ArtistViewSet(BaseAPIViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filter_class = ArtistFilter


class AlbumViewSet(BaseAPIViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filter_class = AlbumFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("artist").prefetch_related("tracks")


class TrackViewSet(BaseAPIViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    filter_class = TrackFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("album", "album__artist")



class PlaylistSet(BaseAPIViewSet,viewsets.ModelViewSet):

    
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        queryset = Playlist.objects.all()
        return queryset

    def create(self,request,*args, **kwargs):
        data= request.data
        playlist_data, created =Playlist.objects.get_or_create(name=data["name"])
        playlist_id=Playlist.objects.get(name=data["name"]).id
        track_sequence=1
        for track in data.get("tracks"):
            track['track_sequence']=track_sequence+1
            track_name=Track.objects.filter(id=track.get("track"))
            track_id=[i.id for i in track_name]
            for seq in track_id:
                sequence_created, created=SequenceTrack.objects.get_or_create(playlist_id=playlist_id,track_id=seq,track_sequence=track.get("track_sequence"))
            for track in track_name:
                playlist_data.tracks.add(track.id)

        serializer=PlaylistSerializer(playlist_data,context={'request': request})
        return Response(serializer.data,status=201)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data,status=204)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)

class AddPlaylistView(CreateView):
    model = Playlist
    form_class = CreatePlaylistForm
    template_name = 'grunge/create_playlist.html'


    def get_context_data(self, **kwargs):
        context = super(AddPlaylistView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PlaylistCreateForm(self.request.POST)
        else:
            context['formset'] = PlaylistCreateForm()
        return context

    def post(self, request, *args, **kwargs):
        formset = PlaylistCreateForm(request.POST)
        if formset.is_valid():
            for form in formset:
                name =form.cleaned_data.get('name')
                track = form.cleaned_data.get('track')
                track_sequence = form.cleaned_data.get('track_sequence')
                playlist_data, created =Playlist.objects.get_or_create(name=name)
                playlist_id=Playlist.objects.get(name=name).id
                track_name=Track.objects.get(id=track).id
                SequenceTrack.objects.get_or_create(playlist_id=playlist_id,track_id=track_name,track_sequence=track_sequence)
                playlist_data.tracks.add(track_name)
            return redirect('playlist_detail',pk=playlist_id)
        else:
            return render(request, 'grunge/create_playlist.html', context={"formset":formset})

 

class PlayListView(ListView):
 
    model = Playlist
    context_object_name = 'playlist_summary'
    template_name = 'grunge/playlist_summary.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PlayListView, self).get_context_data(**kwargs)
        context['form'] = PlayListForm()
        return context


class PlaylistDeleteView(DeleteView):
    # specify the model you want to use
    model = Playlist
    success_url = reverse_lazy('playlist_list')
    template_name = "grunge/playlist_summary.html"


class playlistUpdateName(UpdateView):
    model = Playlist
    fields= ["name"]
    template_name = 'grunge/playlist_summary.html'
    success_url=reverse_lazy('playlist_list')

class PlayListDetail(DetailView):

    model = Playlist
    context_object_name = 'playlist_detail'
    template_name = 'grunge/playlist_detail.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PlayListDetail, self).get_context_data(**kwargs)
        qs = SequenceTrack.objects.filter(playlist=self.object.id)
        order_by = self.request.GET.get('order_by')
        qs = qs.order_by("track_sequence")
        paginator=Paginator(qs, 5)
        page_number = self.request.GET.get('page')
        context['sequence_tracks_list'] = paginator.get_page(page_number)
        context['playlist'] = self.object
        return context



class PlayUpdateView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PlayUpdateView, self).dispatch(request, *args, **kwargs)

    def put(self,request,playlist_id):
        # import pdb;pdb.set_trace()
        # print(">>>>>>>",request)
        data=json.load(request)
        track=data.get('track_name')
        sequence=data.get('sequence')
        previous_sequence=data.get('previous_sequence')
        check_same_sequence_exist=SequenceTrack.objects.filter(playlist_id=playlist_id,track_sequence=sequence)
        if check_same_sequence_exist:
             return JsonResponse(data={"error":"sequence already exist"},status=401)
        track_detail=SequenceTrack.objects.filter(playlist_id=playlist_id,track_id=track)
        track_detail.update(track_sequence=sequence)
        return JsonResponse(data,safe=False)





    

