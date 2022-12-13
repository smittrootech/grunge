from uuid import uuid4

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


class UUIDManager(models.Manager):
    def get_by_natural_key(self, uuid):
        return self.get(uuid=uuid)


class UUIDModel(models.Model):
    uuid = models.UUIDField(verbose_name="UUID", default=uuid4, unique=True)
    objects = UUIDManager()

    class Meta:
        abstract = True

    def natural_key(self):
        return (self.uuid,)


class Artist(UUIDModel):
    name = models.CharField(max_length=100, help_text=_("The artist name"))

    class Meta:
        ordering = ("name",)
        indexes = (models.Index(fields=("name",)),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("admin:grunge_artist_change", kwargs={"object_id": self.pk})


class Album(UUIDModel):
    name = models.CharField(max_length=100, help_text=_("The album name"))
    year = models.PositiveSmallIntegerField(
        help_text=_("The year the album was released")
    )
    artist = models.ForeignKey(
        Artist,
        help_text=_("The artist that produced the album"),
        related_name="albums",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ("artist", "year", "name")
        indexes = (models.Index(fields=("artist", "year", "name")),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("admin:grunge_album_change", kwargs={"object_id": self.pk})


class Track(UUIDModel):
    name = models.CharField(max_length=100, help_text=_("The track name"))
    album = models.ForeignKey(
        Album,
        help_text=_("The album this track appears on"),
        related_name="tracks",
        on_delete=models.CASCADE,
    )
    number = models.PositiveSmallIntegerField(
        help_text=_("The track number on the album")
    )

    class Meta:
        ordering = ("number", "name")
        indexes = (models.Index(fields=("number", "name")),)
        constraints = (
            models.UniqueConstraint(
                fields=("album", "number"), name="unique_album_number"
            ),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("admin:grunge_track_change", kwargs={"object_id": self.pk})


class Playlist(UUIDModel):
    name = models.CharField(max_length=100, help_text=_("The playlist name"))
    tracks=models.ManyToManyField(Track, related_name= "tracks_in_playlist",blank=True,through='SequenceTrack')

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class SequenceTrack(UUIDModel):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE,related_name="sequence_track")
    track = models.ForeignKey(Track, on_delete=models.CASCADE,related_name="sequence_track")
    track_sequence = models.IntegerField(default=1)

    def __str__(self):
        return self.playlist.name

