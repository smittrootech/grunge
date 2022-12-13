from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from .viewsets import AlbumViewSet, ArtistViewSet, TrackViewSet,PlaylistSet,AddPlaylistView,PlayListDetail,PlayListView,PlayUpdateView ,PlaylistDeleteView,playlistUpdateName

urlpatterns = []


if settings.DJANGO_ADMIN_ENABLED:
    urlpatterns += [
        re_path("^$", RedirectView.as_view(url="/admin/", permanent=True)),
        path("admin/", admin.site.urls),
    ]

if settings.DJANGO_API_ENABLED:
    api_router = DefaultRouter(trailing_slash=False)
    api_router.register("artists", ArtistViewSet)
    api_router.register("albums", AlbumViewSet)
    api_router.register("tracks", TrackViewSet)
    api_router.register("playlists", PlaylistSet, basename='playlist')


    

    urlpatterns += [
        path("api/<version>/", include(api_router.urls)),
        path('addplaylistview/', AddPlaylistView.as_view(), name='playlist_create'),
        path('playlistdetail/<int:pk>/', PlayListDetail.as_view(), name='playlist_detail'),
        path('playlistsummary/', PlayListView.as_view(), name='playlist_list'),
        path('playlistdeletion/<pk>/', PlaylistDeleteView.as_view(), name='playlist_delete'),
        path('playlistUpdate/<int:playlist_id>/', PlayUpdateView.as_view(), name='playlist_update'),
        path('<pk>/playlistupdatename/', playlistUpdateName.as_view(), name='playlist_name_update')
    ]
