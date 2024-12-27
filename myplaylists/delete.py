from locust import HttpUser, TaskSet, SequentialTaskSet, task
from common.utils import salt, LOGIN_INFO
import random

create_playlist = []

class UserBehavior(HttpUser):
    def createPlaylist(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        locust_identifier = 'Locust Test Playlist ' + salt()

        response = self.client.post(
            '/api/my-playlists',
            {
                'playlistName': locust_identifier,
                'description': locust_identifier,
                'enumMode': 'public',
                'playlistCreate': None,
            },
            headers=headers
        )
        create_playlist.append(response.json()['playlist'])

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['bao']
        )
        self.accessToken = response.json().get('accessToken')

        for i in range(5):
            self.createPlaylist()

    def on_stop(self):
        response = self.client.post(
            "/api/auth/login",
            LOGIN_INFO['bao']
        )
        accessToken = response.json().get('accessToken')
        headers = {'Authorization': f'Bearer {accessToken}'}

        while create_playlist:
            id = create_playlist.pop()['_id']
            self.client.delete(
                f'/api/my-playlists/{id}',
                headers=headers
            )
            print(len(create_playlist))

    @task
    class Flow(SequentialTaskSet):
        def createPlaylist(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            locust_identifier = 'Locust Test Playlist ' + salt()

            response = self.client.post(
                '/api/my-playlists',
                {
                    'playlistName': locust_identifier,
                    'description': locust_identifier,
                    'enumMode': 'public',
                    'playlistCreate': None,
                },
                headers=headers,
                name='/re-supply'
            )
            create_playlist.append(response.json()['playlist'])

        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['bao']
            )
            self.accessToken = response.json().get('accessToken')
            self.userId = response.json().get('userId')
            
        @task
        def getAllUserPlaylist(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                f'/api/my-playlists/user/{self.userId}',
                headers=headers,
                name='/user-playlists'
            )

            removed_playlist = random.choice(create_playlist)
            self.playlist_id = removed_playlist['_id']
            create_playlist.remove(removed_playlist)

        @task
        def deletePlaylist(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.delete(
                f'/api/my-playlists/{self.playlist_id}',
                headers=headers,
                name='/deleted-playlists'
            )
            
            self.createPlaylist()