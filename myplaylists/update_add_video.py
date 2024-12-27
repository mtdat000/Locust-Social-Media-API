from locust import HttpUser, TaskSet, SequentialTaskSet, task
from common.utils import salt, LOGIN_INFO
import random

create_playlist = []

class UserBehavior(HttpUser):
    def createVideo(self):
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

        for i in range(10):
            self.createVideo()

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

            self.playlist_id = random.choice(create_playlist)['_id']

        @task
        def getAllVideo(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/videos/',
                params={
                    'enumMode': 'public'
                },
                headers=headers
            )
            
            self.video_id = random.choice(response.json()['videos'])['_id']

        @task
        def updateAddVideo(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.put(
                f'/api/my-playlists/{self.playlist_id}/add-video',
                {
                    'videoId': self.video_id,
                },
                headers=headers,
                name='/video-added'
            )