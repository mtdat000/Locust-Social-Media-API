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
        def increaseVideoView(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.post(
                f'/api/videos/{self.video_id}/view',
                headers=headers,
                name='/increase-view'
            )