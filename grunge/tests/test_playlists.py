from unittest import skip
from furl import furl
from uuid import UUID

from . import BaseAPITestCase
from rest_framework import status
from rest_framework.reverse import reverse as drf_reverse
import json
import requests

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
    

    def test_create_playlist(self):

            data =   { "name": "rock_musica",
                        "tracks": [
                            {
                                    "track": 3041
                            },
                            {
                                    "track": 1158
                            }
                        ]
                     }

            response = requests.post(
                "http://127.0.0.1:8000/api/v1/playlists",
                data=json.dumps(data),
                headers={"Content-Type": "application/json"}
            )
            self.assertEqual(201, response.status_code)




    def test_update_playlist(self):
        # url = drf_reverse(
        #     "playlist-detail", kwargs={"version": self.version, "uuid": self.playlist_uuid}
        # )
        # r = self.client.get(url)
        data={"name": "Melody",
                "tracks": [
                            {
                                "track_sequence": 1,
                                "track": 3041
                            },
                            {
                                "track_sequence": 2,
                                "track": 1158
                            }
                        ]
            }

        response = requests.patch(
                "http://127.0.0.1:8000/api/v1/playlists/"+str(self.playlist_uuid),
                data=json.dumps(data),
                headers={"Content-Type": "application/json"}
            )
        if response.status_code ==200:
            self.assertEqual(200, response.status_code)
        else:
            self.assertEqual(204, response.status_code)

    def test_delete_playlist(self):
        # Should be able to delete a playlist by `uuid`.
        response = requests.delete(
                "http://127.0.0.1:8000/api/v1/playlists/"+str(self.playlist_uuid),
                headers={"Content-Type": "application/json"}
            )
        print(response)
        self.assertEqual(204, response.status_code)
