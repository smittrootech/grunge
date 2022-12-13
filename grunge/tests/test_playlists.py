from unittest import skip
from furl import furl
from uuid import UUID

from . import BaseAPITestCase
from rest_framework import status
from rest_framework.reverse import reverse as drf_reverse


class PlaylistTests(BaseAPITestCase):
    def setUp(self):
        self.playlist_name = "Melody"
        self.playlist_uuid = UUID("03af729d-3a37-43b6-b170-101c56e95229")
        # self.album_uuid = UUID("b4fee0db-0c93-4470-96b3-cebd158033a0")


    def test_list_playlists(self):
        url = drf_reverse("playlist-list", kwargs={"version": self.version})
        r = self.client.get(url)
        print(r.data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["count"], 1)


    def test_search_playlists(self):
        url = drf_reverse("playlist-list", kwargs={"version": self.version})
        url = furl(url).set({"name": self.playlist_name}).url
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["count"], 1)
        self.assertEqual(r.data["results"][0]["uuid"], self.playlist_uuid)




    def test_get_playlist(self):
        # Should be able to fetch a playlist by its `uuid`.
        url = drf_reverse(
            "playlist-detail", kwargs={"version": self.version, "uuid": self.playlist_uuid}
        )
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["name"], self.playlist_name)
    

    @skip
    def test_create_playlist(self):
        # Should be able to create a playlist with 0 or more tracks.
        raise NotImplementedError("This test case needs to be implemented.")

    @skip
    def test_update_playlist(self):
        # Should be able to change a playlist's `name`, and add, remove,
        # or re-order tracks.
        raise NotImplementedError("This test case needs to be implemented.")

    @skip
    def test_delete_playlist(self):
        # Should be able to delete a playlist by `uuid`.
        raise NotImplementedError("This test case needs to be implemented.")
