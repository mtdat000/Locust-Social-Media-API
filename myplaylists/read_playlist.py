from locust import HttpUser, TaskSet, task, SequentialTaskSet
from common.utils import salt, LOGIN_INFO
import random

create_playlist_id = []

class AdminBehaviour(HttpUser):
    def on_stop(self):
        response = self.client.post(
            "/api/auth/login",
            LOGIN_INFO['admin']
        )
        accessToken = response.json().get('accessToken')
        headers = {'Authorization': f'Bearer {accessToken}'}

        while create_playlist_id:
            id = create_playlist_id.pop()
            self.client.delete(
                f'/api/my-playlists/{id}',
                headers=headers
            )
            print(len(create_playlist_id))

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
                headers=headers
            )
            create_playlist_id.append(response.json()['playlist']['_id'])

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

            response = self.client.get(
                f'/api/my-playlists/user/{self.userId}',
                headers=headers,
                name='/user-playlists'
            )

            if(len(response.json()['playlists']) == 0):
                for i in range(3):
                    self.createPlaylist()

            self.playlist_id = random.choice(response.json()['playlists'])['_id']

        @task
        def getUserPlaylist(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                f'/api/my-playlists/user/{self.userId}',
                headers=headers,
                name='/playlist'
            )