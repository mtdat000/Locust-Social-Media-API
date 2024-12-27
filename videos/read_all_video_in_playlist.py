from locust import HttpUser, TaskSet, SequentialTaskSet, task
from common.utils import salt, LOGIN_INFO
import random

class UserBehavior(HttpUser):
    @task
    class Flow(SequentialTaskSet):
        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['admin']
            )
            self.accessToken = response.json().get('accessToken')
            self.userId = response.json().get('userId')
            
        @task
        def getAllUserPlaylist(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                f'/api/my-playlists/user/{self.userId}',
                headers=headers,
                name='/user-playlist'
            )

            self.playlist_id = random.choice(response.json()['playlists'])['_id']

        @task
        def getAllVideoInPlaylist(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                f'/api/videos/my-playlist/{self.playlist_id}',
                headers=headers,
                name='/videos-in-playlist'
            ) 