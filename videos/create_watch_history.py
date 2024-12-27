from locust import HttpUser, TaskSet, SequentialTaskSet, task
from common.utils import salt, LOGIN_INFO
import random

class UserBehavior(HttpUser):
    def on_stop(self):
        response = self.client.post(
            "/api/auth/login",
            LOGIN_INFO['bao']
        )
        accessToken = response.json().get('accessToken')
        headers = {'Authorization': f'Bearer {accessToken}'}

        self.client.delete(
            f'/api/videos/user/watch-history',
            headers=headers
        )

        print('DONE')

    @task
    class Flow(SequentialTaskSet):
        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['bao']
            )
            self.accessToken = response.json().get('accessToken')
            
        @task
        def getAllVideo(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/videos/',
                headers=headers
            )

            self.video_id = random.choice(response.json()['videos'])['_id']

        @task
        def createWatchHistory(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.post(
                '/api/videos/user/watch-history',
                {
                    'videoId': self.video_id
                },
                headers=headers
            )