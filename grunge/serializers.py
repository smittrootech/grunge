from furl import furl
from rest_framework import serializers
from rest_framework.reverse import reverse as drf_reverse
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .fields import UUIDHyperlinkedIdentityField
from .models import Album, Artist, Track,Playlist,SequenceTrack


class TrackAlbumArtistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="artist-detail")

    class Meta:
        model = Artist
        fields = ("uuid", "url", "name")


class TrackAlbumSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="album-detail")
    artist = TrackAlbumArtistSerializer()

    class Meta:
        model = Album
        fields = ("uuid", "url", "name", "artist")


class MembershipSerializer(serializers.ModelSerializer):
    """Used as a nested serializer by MemberSerializer"""

    # track_name= serializers.CharField(source='track.name')
    track = serializers.SlugRelatedField(queryset = Track.objects.all(),slug_field = 'id')

    class Meta:
        model = SequenceTrack
        fields = ('track_sequence','track')

class TrackSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="track-detail")
    album = TrackAlbumSerializer()


    class Meta:
        model = Track
        fields = ("uuid", "url", "name", "number", "album")


class AlbumTrackSerializer(TrackSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="track-detail")

    class Meta:
        model = Track
        fields = ("uuid", "url", "name", "number")


class AlbumArtistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="artist-detail")

    class Meta:
        model = Artist
        fields = ("uuid", "url", "name")


class AlbumSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="album-detail")
    artist = AlbumArtistSerializer()
    tracks = AlbumTrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ("uuid", "url", "name", "year", "artist", "tracks")


class ArtistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="artist-detail")
    albums_url = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ("uuid", "url", "name", "albums_url")

    def get_albums_url(self, artist):
        path = drf_reverse("album-list", request=self.context["request"])
        return furl(path).set({"artist_uuid": artist.uuid}).url


class PlaylistSerializer(WritableNestedModelSerializer,serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="playlist-detail")
    tracks=MembershipSerializer(source='sequence_track',many=True)

    class Meta:
        model = Playlist
        fields = ("uuid", "url","name","tracks")

